"""Main API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    organizations,
    workspaces,
    agents,
    agent_runs,
    incidents,
    costs,
    quality,
    safety,
    alerts,
    recommendations,
    prompts,
    knowledge,
    workflows,
    analytics,
    audit_logs,
    api_keys,
    notifications,
    admin,
    websocket,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["Workspaces"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
api_router.include_router(agent_runs.router, prefix="/agent-runs", tags=["Agent Runs"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
api_router.include_router(costs.router, prefix="/costs", tags=["Cost Management"])
api_router.include_router(quality.router, prefix="/quality", tags=["Quality"])
api_router.include_router(safety.router, prefix="/safety", tags=["Safety"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["Prompt Library"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Base"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Audit Logs"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["API Keys"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
