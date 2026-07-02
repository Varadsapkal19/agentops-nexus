"""Central registry for all AgentOps Nexus agents."""

from typing import Dict, Optional, Type

from app.agents.base_agent import BaseAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.safety_agent import SafetyAgent
from app.agents.cost_agent import CostGovernanceAgent
from app.agents.quality_agent import QualityAgent
from app.agents.optimization_agent import OptimizationAgent


AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
    "supervisor": SupervisorAgent,
    "safety": SafetyAgent,
    "cost_governance": CostGovernanceAgent,
    "quality": QualityAgent,
    "optimization": OptimizationAgent,
}

_agent_instances: Dict[str, BaseAgent] = {}


def get_agent(agent_type: str) -> Optional[BaseAgent]:
    """Get or create an agent instance by type."""
    if agent_type not in _agent_instances:
        agent_class = AGENT_REGISTRY.get(agent_type)
        if not agent_class:
            return None
        _agent_instances[agent_type] = agent_class()
    return _agent_instances[agent_type]


def get_supervisor() -> SupervisorAgent:
    return get_agent("supervisor")


def get_safety_agent() -> SafetyAgent:
    return get_agent("safety")


def get_cost_agent() -> CostGovernanceAgent:
    return get_agent("cost_governance")


def get_quality_agent() -> QualityAgent:
    return get_agent("quality")


def get_optimization_agent() -> OptimizationAgent:
    return get_agent("optimization")
