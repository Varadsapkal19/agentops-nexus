"""Base Agent class with common functionality."""

import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Type

import structlog
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.core.config import settings

logger = structlog.get_logger()


class AgentTool:
    """Represents a tool an agent can use."""
    
    def __init__(self, name: str, description: str, function: Any, parameters: Dict):
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters
    
    def to_openai_format(self) -> Dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }


class AgentMemory:
    """Agent memory using Qdrant vector database."""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY or None,
        )
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = await self.openai.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=text,
        )
        return response.data[0].embedding
    
    async def store(
        self,
        content: str,
        metadata: Dict[str, Any],
        point_id: Optional[str] = None,
    ) -> str:
        """Store content in vector memory."""
        embedding = await self.embed_text(content)
        point_id = point_id or str(uuid.uuid4())
        
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={"content": content, **metadata},
                )
            ],
        )
        return point_id
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.7,
        filter_conditions: Optional[Any] = None,
    ) -> List[Dict]:
        """Search for relevant memories."""
        embedding = await self.embed_text(query)
        
        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=filter_conditions,
            with_payload=True,
        )
        
        return [
            {
                "id": str(result.id),
                "score": result.score,
                "content": result.payload.get("content", ""),
                "metadata": {k: v for k, v in result.payload.items() if k != "content"},
            }
            for result in results
        ]
    
    async def delete(self, point_id: str) -> None:
        """Delete a memory point."""
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=[point_id],
        )


class AgentMetrics:
    """Track agent performance metrics."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.runs = 0
        self.successes = 0
        self.failures = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.total_latency_ms = 0.0
    
    def record_run(self, success: bool, tokens: int, cost: float, latency_ms: float):
        self.runs += 1
        if success:
            self.successes += 1
        else:
            self.failures += 1
        self.total_tokens += tokens
        self.total_cost += cost
        self.total_latency_ms += latency_ms
    
    @property
    def success_rate(self) -> float:
        return self.successes / self.runs if self.runs > 0 else 0.0
    
    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.runs if self.runs > 0 else 0.0


class BaseAgent(ABC):
    """
    Abstract base class for all AgentOps Nexus agents.
    """
    
    name: str = "base_agent"
    description: str = "Base agent"
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    max_retries: int = 3
    memory_collection: str = "governance_memory"
    
    def __init__(self):
        self.tools: List[AgentTool] = []
        self.memory = AgentMemory(self.memory_collection)
        self.metrics = AgentMetrics(self.name)
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._register_tools()
        logger.info("Agent initialized", agent=self.name, model=self.model)
    
    @abstractmethod
    def _register_tools(self) -> None:
        """Register agent-specific tools."""
        pass
    
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task."""
        pass
    
    def add_tool(self, tool: AgentTool) -> None:
        self.tools.append(tool)
    
    def get_tool_definitions(self) -> List[Dict]:
        return [tool.to_openai_format() for tool in self.tools]
    
    async def execute_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a specific tool by name."""
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        logger.info("Executing tool", agent=self.name, tool=tool_name)
        
        if callable(tool.function):
            import asyncio
            if asyncio.iscoroutinefunction(tool.function):
                return await tool.function(**arguments)
            else:
                return tool.function(**arguments)
        
        raise ValueError(f"Tool function for '{tool_name}' is not callable")
    
    async def chat(
        self,
        messages: List[Dict],
        system_prompt: Optional[str] = None,
        use_tools: bool = True,
    ) -> Dict[str, Any]:
        """Run a chat completion with retry logic."""
        start_time = time.time()
        
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        for attempt in range(self.max_retries):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": full_messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }
                
                if use_tools and self.tools:
                    kwargs["tools"] = self.get_tool_definitions()
                    kwargs["tool_choice"] = "auto"
                
                response = await self.openai.chat.completions.create(**kwargs)
                
                duration_ms = (time.time() - start_time) * 1000
                usage = response.usage
                
                # Calculate cost (approximate)
                cost = self._estimate_cost(
                    usage.prompt_tokens,
                    usage.completion_tokens,
                    self.model,
                )
                
                self.metrics.record_run(
                    success=True,
                    tokens=usage.total_tokens,
                    cost=cost,
                    latency_ms=duration_ms,
                )
                
                return {
                    "content": response.choices[0].message.content,
                    "tool_calls": response.choices[0].message.tool_calls,
                    "usage": {
                        "prompt_tokens": usage.prompt_tokens,
                        "completion_tokens": usage.completion_tokens,
                        "total_tokens": usage.total_tokens,
                    },
                    "cost_usd": cost,
                    "model": self.model,
                    "latency_ms": duration_ms,
                }
                
            except Exception as e:
                logger.warning(
                    "Agent chat attempt failed",
                    agent=self.name,
                    attempt=attempt + 1,
                    error=str(e),
                )
                if attempt == self.max_retries - 1:
                    self.metrics.record_run(False, 0, 0.0, (time.time() - start_time) * 1000)
                    raise
                
                import asyncio
                await asyncio.sleep(2 ** attempt)
        
        raise RuntimeError("Max retries exceeded")
    
    def _estimate_cost(self, prompt_tokens: int, completion_tokens: int, model: str) -> float:
        """Estimate cost in USD based on token usage."""
        pricing = {
            "gpt-4o": {"prompt": 2.50, "completion": 10.00},
            "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
            "gpt-4-turbo": {"prompt": 10.00, "completion": 30.00},
            "claude-3-5-sonnet-20241022": {"prompt": 3.00, "completion": 15.00},
            "claude-3-haiku-20240307": {"prompt": 0.25, "completion": 1.25},
            "gemini-1.5-pro": {"prompt": 1.25, "completion": 5.00},
            "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.30},
        }
        
        model_pricing = pricing.get(model, {"prompt": 2.50, "completion": 10.00})
        cost = (
            prompt_tokens * model_pricing["prompt"] / 1_000_000
            + completion_tokens * model_pricing["completion"] / 1_000_000
        )
        return round(cost, 8)
    
    async def store_memory(
        self,
        content: str,
        memory_type: str,
        organization_id: str,
        extra_metadata: Optional[Dict] = None,
    ) -> str:
        """Store a memory in Qdrant."""
        metadata = {
            "agent_name": self.name,
            "memory_type": memory_type,
            "organization_id": organization_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **(extra_metadata or {}),
        }
        return await self.memory.store(content, metadata)
    
    async def recall_memories(
        self,
        query: str,
        organization_id: str,
        memory_type: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict]:
        """Recall relevant memories from Qdrant."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        conditions = [
            FieldCondition(key="organization_id", match=MatchValue(value=organization_id))
        ]
        
        if memory_type:
            conditions.append(
                FieldCondition(key="memory_type", match=MatchValue(value=memory_type))
            )
        
        filter_conditions = Filter(must=conditions) if conditions else None
        
        return await self.memory.search(
            query=query,
            limit=limit,
            filter_conditions=filter_conditions,
        )
