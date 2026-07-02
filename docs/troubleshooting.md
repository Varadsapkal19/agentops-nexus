# Troubleshooting Guide

This guide details resolutions for common system errors, infrastructure failures, and vector database collection sync issues.

---

## 1. Qdrant Connection or Initialization Failures

### Symptom
*   FastAPI backend fails to boot or loops during startup.
*   Logs report `qdrant_client.http.exceptions.UnexpectedResponse: Status code: 404`.

### Resolution
*   Verify that `QDRANT_URL` in your `.env` matches the Qdrant instance.
*   If using local Docker, make sure the `agentops_qdrant_dev` container has finished booting.
*   You can manually initialize collections by running our setup helper:
    ```bash
    python -c "import asyncio; from app.utils.qdrant_setup import initialize_qdrant_collections; asyncio.run(initialize_qdrant_collections())"
    ```

---

## 2. Celery Worker Sync Issues

### Symptom
*   Background recommendations, safety audits, or hourly cost jobs are not executing.
*   No logs from Celery workers.

### Resolution
*   Ensure the Redis cache is running and accessible.
*   Verify Celery worker configuration:
    ```bash
    celery -A app.celery_app status
    ```
*   To start a debug worker process locally:
    ```bash
    celery -A app.celery_app worker --loglevel=debug
    ```

---

## 3. Database Migration Errors

### Symptom
*   FastAPI logs trace errors reporting missing database columns or tables.

### Resolution
*   Run the Alembic database migrations:
    ```bash
    alembic upgrade head
    ```
*   If you need to reset the schema during development:
    ```bash
    alembic downgrade base
    alembic upgrade head
    ```
