"""Celery application configuration."""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "agentops_nexus",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.workers.agent_tasks",
        "app.workers.analytics_tasks",
        "app.workers.notification_tasks",
        "app.workers.optimization_tasks",
        "app.workers.safety_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_soft_time_limit=300,
    task_time_limit=600,
    result_expires=3600,
)

celery_app.conf.beat_schedule = {
    "collect-agent-metrics": {
        "task": "app.workers.analytics_tasks.collect_agent_metrics",
        "schedule": 60.0,  # Every minute
    },
    "run-health-checks": {
        "task": "app.workers.agent_tasks.run_health_checks",
        "schedule": 300.0,  # Every 5 minutes
    },
    "generate-daily-reports": {
        "task": "app.workers.analytics_tasks.generate_daily_report",
        "schedule": crontab(hour=0, minute=0),  # Daily at midnight
    },
    "run-optimization-cycle": {
        "task": "app.workers.optimization_tasks.run_optimization_cycle",
        "schedule": crontab(hour="*/4"),  # Every 4 hours
    },
    "check-safety-compliance": {
        "task": "app.workers.safety_tasks.check_compliance",
        "schedule": crontab(hour="*/2"),  # Every 2 hours
    },
}
