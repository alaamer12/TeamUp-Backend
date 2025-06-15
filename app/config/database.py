import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.models.team_request import TeamRequest

# Initialize logger
logger = logging.getLogger(__name__)


class Database:
    """MongoDB database connection manager."""

    client: Optional[AsyncIOMotorClient] = None

    @classmethod
    async def connect(cls, mongodb_uri: str) -> None:
        """
        Connects to MongoDB using the provided URI.
        
        Args:
            mongodb_uri: MongoDB connection string
        """
        try:
            cls.client = AsyncIOMotorClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                socketTimeoutMS=45000,
                family=4  # Force IPv4
            )

            # Initialize Beanie with the document models
            db_name = mongodb_uri.split("/")[-1].split("?")[0]  # Extract DB name from URI
            await init_beanie(
                database=cls.client[db_name],
                document_models=[TeamRequest]
            )

            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def close(cls) -> None:
        """Closes the MongoDB connection."""
        if cls.client:
            cls.client.close()
            cls.client = None
            logger.info("Closed MongoDB connection")
