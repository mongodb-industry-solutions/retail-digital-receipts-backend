# settings.py ─ global configuration

import logging
from pydantic_settings import BaseSettings
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Mandatory values
    mongodb_uri: str
    database_name: str

    # Azure Blob Storage with Managed Identity
    azure_blob_account_url: str          # https://<account>.blob.core.windows.net/
    azure_blob_container_name: str       # retail-invoices

    # Misc
    azure_metadata_endpoint: str
    origins: str                         # CORS

    model_config = {
        "env_file": ".env",
        "extra": "forbid",
    }


try:
    settings = Settings()

    logger.info("MongoDB URI: %s", settings.mongodb_uri)
    logger.info("Database: %s", settings.database_name)
    logger.info("Blob account URL: %s", settings.azure_blob_account_url)
    logger.info("Blob container: %s", settings.azure_blob_container_name)
    logger.info("Metadata endpoint: %s", settings.azure_metadata_endpoint)
    logger.info("CORS origins: %s", settings.origins)

except ValidationError as err:
    logger.error("Settings validation error: %s", err)
    raise

except Exception as exc:
    logger.error("Error loading settings: %s", exc)
    raise
