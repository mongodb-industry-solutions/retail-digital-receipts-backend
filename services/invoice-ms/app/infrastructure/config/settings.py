import logging
from pydantic_settings import BaseSettings
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    mongodb_uri: str
    database_name: str
    
    # Add fields for the extra env vars you have in .env:
    azure_storage_connection_string: str
    # If 'origins' is just a single string, do this:
    origins: str
    # Or if you intend it to be a list:
    # origins: list[str] = []

    # Pydantic v2 approach to config:
    model_config = {
        "env_file": ".env",
        # "extra": "allow",  # use this if you want to IGNORE unexpected env vars
        "extra": "forbid",   # or keep forbid if you want an error on unexpected env vars
    }

try:
    settings = Settings()
    # Log or use them:
    logger.info("MongoDB URI: %s", settings.mongodb_uri)
    logger.info("Database Name: %s", settings.database_name)
    logger.info("Azure Storage Connection: %s", settings.azure_storage_connection_string)
    logger.info("Origins: %s", settings.origins)

except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise

except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    raise
