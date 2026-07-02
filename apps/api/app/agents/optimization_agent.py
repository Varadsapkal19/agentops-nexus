"""Optimization Agent for prompt and workflow improvements."""

from typing import Any, Dict, List
import structlog

from app.agents.base_agent import AgentTool, BaseAgent
from app.core.config import settings

logger = structlog.get_logger()


class OptimizationAgent(BaseAgent):
    """Agent for optimizing prompts, models, and workflows."""
    
    name = "optimization"
    description = "AI prompt and workflow optimization agent"
    model = settings.OPENAI_MODEL
    temperature = 0.5
    memory_collection = "optimization_memory"
    
    SYSTEM_PROMPT = """
You are the Optimization Agent for AgentOps Nexus.

Your responsibilities:
1. Analyze and improve system prompts
2. Optimize agent configurations
3. Identify workflow bottlenecks
4. Suggest model parameter tuning
5. A/B test prompt variations
6. Recommend architecture improvements

Focus on measurable improvements with clear metrics.
"""
    
    def _register_tools(self) -> None:
        self.add_tool(AgentTool(
            name="optimize_prompt",
            description="Optimize a system prompt for better performance",
            function=self._optimize_prompt,
            parameters={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "use_case": {"type": "string"},
                    "quality_scores": {"type": "object"},
                },
                "required": ["prompt", "use_case"],
            },
        ))
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        agent_id = input_data.get("agent_id", "")
        organization_id = input_data.get("organization_id", "")
        current_prompt = input_data.get("system_prompt", "")
        performance_data = input_data.get("performance_data", {})
        
        messages = [
            {
                "role": "user",
                "content": f"""
Optimize the following AI agent configuration:

Agent ID: {agent_id}
Current System Prompt: {current_prompt[:1000]}
Performance Data: {performance_data}

Provide:
1. Analysis of current prompt effectiveness
2. Specific improvements to the prompt
3. Optimized prompt version
4. Expected improvements (with % estimates)
5. Configuration recommendations (temperature, max_tokens, model)
""",
            }
        ]
        
        result = await self.chat(messages, system_prompt=self.SYSTEM_PROMPT)
        
        await self.store_memory(
            content=f"Optimization for agent {agent_id}: {result['content'][:500]}",
            memory_type="optimization",
            organization_id=organization_id,
            extra_metadata={"agent_id": agent_id},
        )
        
        return {
            "optimization_suggestions": result["content"],
            "tokens_used": result["usage"]["total_tokens"],
            "cost_usd": result["cost_usd"],
        }
    
    async def _optimize_prompt(self, prompt: str, use_case: str, quality_scores: Dict = None) -> Dict:
        messages = [
            {
                "role": "user",
                "content": f"Improve this prompt for {use_case}:\n\n{prompt}\n\nQuality scores: {quality_scores}",
            }
        ]
        result = await self.chat(messages, use_tools=False)
        return {"optimized_prompt": result["content"], "improvements": []}
