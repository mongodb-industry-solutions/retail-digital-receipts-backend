import logging
from pydantic_settings import BaseSettings
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    mongodb_uri: str
    database_name: str
    azure_storage_connection_string: str
    origins: str
    azure_metadata_endpoint: str 

    model_config = {
        "env_file": ".env",
        "extra": "forbid",
    }

try:
    settings = Settings()
    logger.info("MongoDB URI: %s", settings.mongodb_uri)
    logger.info("Database Name: %s", settings.database_name)
    logger.info("Azure Storage Connection: %s", settings.azure_storage_connection_string)
    logger.info("Origins: %s", settings.origins)
    logger.info("Azure Metadata Endpoint: %s", settings.azure_metadata_endpoint)

except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise

except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    raise
