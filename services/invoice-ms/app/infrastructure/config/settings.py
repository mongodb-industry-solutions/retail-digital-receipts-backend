import logging
from pydantic_settings import BaseSettings
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Required environment variables
    mongodb_uri: str
    database_name: str
    azure_storage_connection_string: str
    azure_blob_container_name: str   # Added to support Azure Blob uploads
    azure_metadata_endpoint: str
    origins: str  # CORS settings, e.g. "*"

    # Pydantic settings config
    model_config = {
        "env_file": ".env",
        "extra": "forbid",  # Strict: only allow declared variables
    }

try:
    settings = Settings()
    logger.info("MongoDB URI: %s", settings.mongodb_uri)
    logger.info("Database Name: %s", settings.database_name)
    logger.info("Azure Storage Connection: %s", settings.azure_storage_connection_string)
    logger.info("Azure Blob Container Name: %s", settings.azure_blob_container_name)
    logger.info("Azure Metadata Endpoint: %s", settings.azure_metadata_endpoint)
    logger.info("CORS Origins: %s", settings.origins)

except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise

except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    raise
