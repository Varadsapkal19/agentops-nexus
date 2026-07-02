"""Supervisor Agent - orchestrates all other agents."""

import json
from typing import Any, Dict, List, Optional

import structlog

from app.agents.base_agent import AgentTool, BaseAgent
from app.core.config import settings

logger = structlog.get_logger()


class SupervisorAgent(BaseAgent):
    """
    The main orchestrating agent that governs all other agents.
    Acts as the AI Chief Operating Officer.
    """
    
    name = "supervisor"
    description = "Enterprise AI COO - orchestrates all governance agents"
    model = settings.OPENAI_MODEL
    temperature = 0.3
    memory_collection = "governance_memory"
    
    SYSTEM_PROMPT = """
You are the Supervisor Agent for AgentOps Nexus — an AI Chief Operating Officer (COO) for enterprise AI ecosystems.

Your role is to:
1. Monitor all AI agents across the organization
2. Detect failures, anomalies, and risks
3. Coordinate specialized agents (cost, quality, safety, memory, optimization)
4. Generate actionable recommendations
5. Ensure compliance with policies
6. Learn from past incidents to prevent recurrence

You have access to tools to:
- Analyze agent performance metrics
- Search historical incidents
- Trigger specialized agents
- Create recommendations
- Send alerts

Always:
- Be decisive and actionable
- Prioritize safety and compliance
- Consider cost implications
- Provide clear reasoning
- Reference past incidents when relevant
"""
    
    def _register_tools(self) -> None:
        self.add_tool(AgentTool(
            name="analyze_agent_health",
            description="Analyze the health and performance of an AI agent",
            function=self._analyze_agent_health,
            parameters={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string", "description": "Agent ID to analyze"},
                    "time_window_hours": {"type": "integer", "default": 24},
                },
                "required": ["agent_id"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="search_past_incidents",
            description="Search historical incidents for similar patterns",
            function=self._search_past_incidents,
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "organization_id": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["query", "organization_id"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="create_recommendation",
            description="Create a governance recommendation",
            function=self._create_recommendation,
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "recommendation_type": {"type": "string"},
                    "priority_score": {"type": "number"},
                    "agent_id": {"type": "string"},
                    "organization_id": {"type": "string"},
                },
                "required": ["title", "description", "recommendation_type", "organization_id"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="trigger_safety_check",
            description="Trigger a safety analysis for agent output",
            function=self._trigger_safety_check,
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "agent_id": {"type": "string"},
                    "organization_id": {"type": "string"},
                },
                "required": ["content", "agent_id", "organization_id"],
            },
        ))
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main supervisor execution."""
        organization_id = input_data.get("organization_id", "")
        incident = input_data.get("incident")
        agent_metrics = input_data.get("agent_metrics", [])
        trigger = input_data.get("trigger", "manual")
        
        logger.info(
            "Supervisor running",
            trigger=trigger,
            organization=organization_id,
        )
        
        # Recall relevant past incidents
        past_memories = await self.recall_memories(
            query=f"incident analysis {trigger}",
            organization_id=organization_id,
            limit=3,
        )
        
        # Build context
        context = f"""
Organization: {organization_id}
Trigger: {trigger}
Incident: {json.dumps(incident, indent=2) if incident else 'None'}
Agent Metrics: {json.dumps(agent_metrics, indent=2)}
Past Similar Incidents:\n{json.dumps(past_memories, indent=2)}
"""
        
        messages = [
            {"role": "user", "content": f"Analyze the following situation and provide governance actions:\n{context}"}
        ]
        
        result = await self.chat(messages, system_prompt=self.SYSTEM_PROMPT)
        
        # Store this analysis in memory
        await self.store_memory(
            content=f"Supervisor analysis: {result['content']}",
            memory_type="supervisor_analysis",
            organization_id=organization_id,
            extra_metadata={"trigger": trigger},
        )
        
        return {
            "analysis": result["content"],
            "tool_calls_made": len(result.get("tool_calls") or []),
            "tokens_used": result["usage"]["total_tokens"],
            "cost_usd": result["cost_usd"],
            "latency_ms": result["latency_ms"],
        }
    
    async def _analyze_agent_health(self, agent_id: str, time_window_hours: int = 24) -> Dict:
        """Tool: Analyze agent health metrics."""
        return {
            "agent_id": agent_id,
            "status": "analyzed",
            "time_window_hours": time_window_hours,
            "health_score": 0.85,
            "issues_detected": [],
        }
    
    async def _search_past_incidents(
        self, query: str, organization_id: str, limit: int = 5
    ) -> List[Dict]:
        """Tool: Search past incidents in memory."""
        return await self.recall_memories(
            query=query,
            organization_id=organization_id,
            memory_type="incident",
            limit=limit,
        )
    
    async def _create_recommendation(
        self,
        title: str,
        description: str,
        recommendation_type: str,
        organization_id: str,
        priority_score: float = 0.5,
        agent_id: Optional[str] = None,
    ) -> Dict:
        """Tool: Create a governance recommendation."""
        return {
            "created": True,
            "title": title,
            "type": recommendation_type,
            "priority": priority_score,
        }
    
    async def _trigger_safety_check(self, content: str, agent_id: str, organization_id: str) -> Dict:
        """Tool: Trigger safety analysis."""
        from app.agents.safety_agent import SafetyAgent
        safety_agent = SafetyAgent()
        return await safety_agent.run({
            "content": content,
            "agent_id": agent_id,
            "organization_id": organization_id,
        })
