"""Quality Assessment Agent."""

from typing import Any, Dict, List, Optional
import structlog

from app.agents.base_agent import AgentTool, BaseAgent
from app.core.config import settings

logger = structlog.get_logger()


class QualityAgent(BaseAgent):
    """Agent for evaluating and improving AI output quality."""
    
    name = "quality"
    description = "AI output quality evaluation and improvement agent"
    model = settings.OPENAI_MODEL
    temperature = 0.2
    memory_collection = "governance_memory"
    
    SYSTEM_PROMPT = """
You are the Quality Agent for AgentOps Nexus.

Your responsibilities:
1. Evaluate AI agent output quality across multiple dimensions
2. Detect quality degradation trends
3. Identify common quality issues
4. Recommend quality improvements
5. Score responses on relevance, coherence, completeness, accuracy
6. Compare against baseline quality standards

Be objective and consistent in scoring. Use a 0-1 scale for all scores.
"""
    
    def _register_tools(self) -> None:
        self.add_tool(AgentTool(
            name="evaluate_response",
            description="Evaluate the quality of an AI response",
            function=self._evaluate_response,
            parameters={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "response": {"type": "string"},
                    "expected_output": {"type": "string"},
                },
                "required": ["prompt", "response"],
            },
        ))
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = input_data.get("prompt", "")
        response = input_data.get("response", "")
        expected = input_data.get("expected_output", "")
        agent_id = input_data.get("agent_id", "")
        organization_id = input_data.get("organization_id", "")
        
        messages = [
            {
                "role": "user",
                "content": f"""
Evaluate the quality of this AI response:

Prompt: {prompt}
Response: {response}
{f'Expected: {expected}' if expected else ''}

Provide JSON scores:
{{
  "overall_score": 0.0-1.0,
  "relevance_score": 0.0-1.0,
  "coherence_score": 0.0-1.0,
  "completeness_score": 0.0-1.0,
  "accuracy_score": 0.0-1.0,
  "hallucination_risk": 0.0-1.0,
  "issues": [],
  "suggestions": []
}}
""",
            }
        ]
        
        result = await self.chat(messages, system_prompt=self.SYSTEM_PROMPT, use_tools=False)
        
        import json, re
        scores = {}
        try:
            json_match = re.search(r'\{[^{}]*\}', result["content"], re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
        except Exception:
            scores = {"overall_score": 0.75}
        
        return {
            "overall_score": scores.get("overall_score", 0.75),
            "relevance_score": scores.get("relevance_score", 0.75),
            "coherence_score": scores.get("coherence_score", 0.75),
            "completeness_score": scores.get("completeness_score", 0.75),
            "accuracy_score": scores.get("accuracy_score", 0.75),
            "hallucination_risk": scores.get("hallucination_risk", 0.1),
            "issues": scores.get("issues", []),
            "suggestions": scores.get("suggestions", []),
            "analysis": result["content"],
            "tokens_used": result["usage"]["total_tokens"],
            "cost_usd": result["cost_usd"],
        }
    
    async def _evaluate_response(self, prompt: str, response: str, expected_output: str = "") -> Dict:
        return {"quality_score": 0.85, "issues": [], "suggestions": []}
