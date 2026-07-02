"""Qdrant collections setup and initialization."""

import structlog
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import settings

logger = structlog.get_logger()


async def initialize_qdrant_collections():
    """Create collections in Qdrant if they do not exist."""
    if not settings.QDRANT_URL:
        logger.warning("QDRANT_URL not configured. Skipping Qdrant collection initialization.")
        return

    client = AsyncQdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY or None,
    )
    
    # Vector size: 1536 for text-embedding-3-small, 3072 for text-embedding-3-large
    # Let's support both but default to 3072 for text-embedding-3-large
    vector_size = 3072 if "large" in settings.OPENAI_EMBEDDING_MODEL else 1536
    
    collections = [
        "incident_memory",
        "governance_memory",
        "optimization_memory",
        "prompt_memory",
        "policy_memory",
        "organization_memory",
        "conversation_memory",
        "historical_metrics",
        "knowledge_base"
    ]
    
    for name in collections:
        try:
            exists = await client.collection_exists(collection_name=name)
            if not exists:
                await client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info("Created Qdrant collection", collection=name)
            else:
                logger.debug("Qdrant collection already exists", collection=name)
        except Exception as e:
            logger.error("Failed to initialize Qdrant collection", collection=name, error=str(e))
    
    await client.close()
