from motor.motor_asyncio import AsyncIOMotorClient
from app.infrastructure.config.settings import settings


_client = None  # Internal client instance (shared across the app)
_db = None      # Internal reference to the MongoDB database

def get_db():
    """
    Returns a singleton MongoDB database instance.

    This function ensures that only one instance of AsyncIOMotorClient is created
    and reused throughout the application's lifecycle.

    This is critical for:
    - Performance (avoids unnecessary reconnections)
    - Scalability (prevents exceeding connection limits)
    - Stability (ensures reliable behavior with Change Streams)
    """
    global _client, _db

    if _client is None:
        # Create the MongoDB client only once (lazy initialization)
        _client = AsyncIOMotorClient(settings.mongodb_uri)
        _db = _client[settings.database_name]

    return _db

# Shortcut for modules that need direct access
db = get_db()
