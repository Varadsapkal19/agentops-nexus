"""Cost Governance Agent."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone, timedelta

import structlog

from app.agents.base_agent import AgentTool, BaseAgent
from app.core.config import settings

logger = structlog.get_logger()


class CostGovernanceAgent(BaseAgent):
    """Agent for monitoring and optimizing AI costs."""
    
    name = "cost_governance"
    description = "AI cost monitoring, budgeting, and optimization agent"
    model = settings.OPENAI_MODEL
    temperature = 0.2
    memory_collection = "governance_memory"
    
    SYSTEM_PROMPT = """
You are the Cost Governance Agent for AgentOps Nexus.

Your responsibilities:
1. Monitor token usage and costs across all agents
2. Detect cost anomalies and budget overruns
3. Recommend cost optimization strategies
4. Suggest model downgrades when quality allows
5. Identify inefficient prompts and workflows
6. Forecast future costs
7. Enforce budget limits

Always balance cost with quality - don't sacrifice critical functionality to save money.
"""
    
    def _register_tools(self) -> None:
        self.add_tool(AgentTool(
            name="analyze_cost_trend",
            description="Analyze cost trends for an organization",
            function=self._analyze_cost_trend,
            parameters={
                "type": "object",
                "properties": {
                    "organization_id": {"type": "string"},
                    "days": {"type": "integer", "default": 30},
                },
                "required": ["organization_id"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="check_budget_status",
            description="Check current budget utilization",
            function=self._check_budget_status,
            parameters={
                "type": "object",
                "properties": {"organization_id": {"type": "string"}},
                "required": ["organization_id"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="suggest_model_optimization",
            description="Suggest cheaper models for specific use cases",
            function=self._suggest_model_optimization,
            parameters={
                "type": "object",
                "properties": {
                    "current_model": {"type": "string"},
                    "use_case": {"type": "string"},
                    "quality_requirement": {"type": "number"},
                },
                "required": ["current_model", "use_case"],
            },
        ))
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        organization_id = input_data.get("organization_id", "")
        cost_data = input_data.get("cost_data", {})
        
        past_memories = await self.recall_memories(
            query="cost optimization budget",
            organization_id=organization_id,
            limit=3,
        )
        
        messages = [
            {
                "role": "user",
                "content": f"""
Analyze costs for organization {organization_id}:

Cost Data: {cost_data}
Past Recommendations: {past_memories}

Provide:
1. Cost analysis and trends
2. Budget utilization status
3. Top cost drivers
4. Optimization recommendations (with estimated savings)
5. Risk assessment
""",
            }
        ]
        
        result = await self.chat(messages, system_prompt=self.SYSTEM_PROMPT)
        
        await self.store_memory(
            content=f"Cost analysis: {result['content']}",
            memory_type="cost_analysis",
            organization_id=organization_id,
        )
        
        return {
            "analysis": result["content"],
            "tokens_used": result["usage"]["total_tokens"],
            "cost_usd": result["cost_usd"],
        }
    
    async def _analyze_cost_trend(self, organization_id: str, days: int = 30) -> Dict:
        return {"trend": "stable", "avg_daily_cost": 12.50, "total_cost": days * 12.50}
    
    async def _check_budget_status(self, organization_id: str) -> Dict:
        return {"budget_usd": 500.0, "spent_usd": 187.50, "utilization_pct": 37.5}
    
    async def _suggest_model_optimization(
        self, current_model: str, use_case: str, quality_requirement: float = 0.8
    ) -> Dict:
        suggestions = {
            "gpt-4o": "gpt-4o-mini" if quality_requirement < 0.9 else "gpt-4o",
            "claude-3-5-sonnet-20241022": "claude-3-haiku-20240307" if quality_requirement < 0.85 else "claude-3-5-sonnet-20241022",
            "gemini-1.5-pro": "gemini-1.5-flash" if quality_requirement < 0.85 else "gemini-1.5-pro",
        }
        suggested = suggestions.get(current_model, current_model)
        return {
            "current_model": current_model,
            "suggested_model": suggested,
            "estimated_savings_pct": 70 if suggested != current_model else 0,
        }
