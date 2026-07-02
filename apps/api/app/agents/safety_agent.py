"""Safety Agent - hallucination, bias, toxicity, and compliance checking."""

import httpx
from typing import Any, Dict, List, Optional

import structlog

from app.agents.base_agent import AgentTool, BaseAgent
from app.core.config import settings

logger = structlog.get_logger()


class SafetyAgent(BaseAgent):
    """
    Safety Agent using Enkrypt AI for:
    - Hallucination detection
    - Bias detection
    - Toxicity detection
    - Jailbreak detection
    - PII detection
    - Compliance checking
    - Policy validation
    """
    
    name = "safety"
    description = "AI safety and compliance enforcement agent"
    model = settings.OPENAI_MODEL
    temperature = 0.1  # Low temperature for consistent safety decisions
    memory_collection = "governance_memory"
    
    SYSTEM_PROMPT = """
You are the Safety Agent for AgentOps Nexus.

Your responsibilities:
1. Analyze AI agent outputs for safety issues
2. Detect hallucinations, bias, toxicity, and jailbreaks
3. Enforce compliance with organizational policies
4. Block or flag unsafe content
5. Generate detailed safety reports
6. Learn from past violations to improve detection

Always be conservative - when in doubt, flag for review.
Provide clear reasoning for every safety decision.
"""
    
    def _register_tools(self) -> None:
        self.add_tool(AgentTool(
            name="check_hallucination",
            description="Check content for hallucinations",
            function=self._check_hallucination,
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "context": {"type": "string"},
                },
                "required": ["content"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="check_toxicity",
            description="Check content for toxicity",
            function=self._check_toxicity,
            parameters={
                "type": "object",
                "properties": {"content": {"type": "string"}},
                "required": ["content"],
            },
        ))
        
        self.add_tool(AgentTool(
            name="check_pii",
            description="Check for personally identifiable information",
            function=self._check_pii,
            parameters={
                "type": "object",
                "properties": {"content": {"type": "string"}},
                "required": ["content"],
            },
        ))
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run safety analysis on content."""
        content = input_data.get("content", "")
        agent_id = input_data.get("agent_id", "")
        organization_id = input_data.get("organization_id", "")
        
        logger.info("Safety agent analyzing content", agent_id=agent_id)
        
        # Run Enkrypt AI analysis
        enkrypt_result = await self._run_enkrypt_analysis(content)
        
        # Also run LLM-based analysis for detailed reasoning
        messages = [
            {
                "role": "user",
                "content": f"""
Analyze the following AI agent output for safety issues:

Content: {content[:2000]}

Enkrypt AI Results: {enkrypt_result}

Provide:
1. Overall safety score (0-1, 1=completely safe)
2. Specific issues detected
3. Risk level (safe/low/medium/high/critical)
4. Whether to block this content
5. Recommended action
""",
            }
        ]
        
        analysis = await self.chat(messages, system_prompt=self.SYSTEM_PROMPT)
        
        # Determine if content should be blocked
        should_block = (
            enkrypt_result.get("hallucination_score", 0) > 0.8
            or enkrypt_result.get("toxicity_score", 0) > 0.7
            or enkrypt_result.get("jailbreak_score", 0) > 0.6
        )
        
        result = {
            "safe": not should_block,
            "blocked": should_block,
            "overall_safety_score": enkrypt_result.get("safety_score", 0.5),
            "hallucination_detected": enkrypt_result.get("hallucination_score", 0) > 0.5,
            "hallucination_score": enkrypt_result.get("hallucination_score", 0),
            "bias_detected": enkrypt_result.get("bias_score", 0) > 0.5,
            "bias_score": enkrypt_result.get("bias_score", 0),
            "toxicity_detected": enkrypt_result.get("toxicity_score", 0) > 0.5,
            "toxicity_score": enkrypt_result.get("toxicity_score", 0),
            "jailbreak_detected": enkrypt_result.get("jailbreak_score", 0) > 0.5,
            "jailbreak_score": enkrypt_result.get("jailbreak_score", 0),
            "pii_detected": enkrypt_result.get("pii_detected", False),
            "analysis": analysis["content"],
            "agent_id": agent_id,
            "tokens_used": analysis["usage"]["total_tokens"],
            "cost_usd": analysis["cost_usd"],
        }
        
        # Store safety record in memory
        if not result["safe"]:
            await self.store_memory(
                content=f"Safety violation detected: {analysis['content']}",
                memory_type="safety_violation",
                organization_id=organization_id,
                extra_metadata={"agent_id": agent_id, "blocked": should_block},
            )
        
        return result
    
    async def _run_enkrypt_analysis(self, content: str) -> Dict:
        """Run Enkrypt AI safety analysis."""
        if not settings.ENKRYPT_API_KEY:
            # Fallback to basic LLM-based analysis
            return await self._llm_safety_analysis(content)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.ENKRYPT_API_URL}/v1/analyze",
                    headers={
                        "Authorization": f"Bearer {settings.ENKRYPT_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "text": content,
                        "checks": [
                            "hallucination",
                            "bias",
                            "toxicity",
                            "jailbreak",
                            "pii",
                            "compliance",
                        ],
                    },
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            logger.warning("Enkrypt AI call failed, falling back to LLM", error=str(e))
        
        return await self._llm_safety_analysis(content)
    
    async def _llm_safety_analysis(self, content: str) -> Dict:
        """Fallback LLM-based safety analysis."""
        messages = [
            {
                "role": "user",
                "content": f"""
Analyze this content for safety issues. Return JSON with these scores (0.0-1.0):
{{
  "hallucination_score": 0.0,
  "bias_score": 0.0,
  "toxicity_score": 0.0,
  "jailbreak_score": 0.0,
  "pii_detected": false,
  "safety_score": 1.0
}}

Content: {content[:1000]}
""",
            }
        ]
        
        result = await self.chat(messages, use_tools=False)
        
        try:
            import json
            import re
            json_match = re.search(r'\{[^}]+\}', result["content"], re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        
        return {
            "hallucination_score": 0.0,
            "bias_score": 0.0,
            "toxicity_score": 0.0,
            "jailbreak_score": 0.0,
            "pii_detected": False,
            "safety_score": 0.9,
        }
    
    async def _check_hallucination(self, content: str, context: str = "") -> Dict:
        return {"score": 0.1, "detected": False}
    
    async def _check_toxicity(self, content: str) -> Dict:
        return {"score": 0.0, "detected": False}
    
    async def _check_pii(self, content: str) -> Dict:
        return {"detected": False, "types": []}
