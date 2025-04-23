# settings.py — recommendation-ms
import logging
from pydantic_settings import BaseSettings
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # MongoDB
    mongodb_uri: str
    database_name: str

    # Atlas Vector Search
    vector_index_name: str = "product_vector_index"
    embedding_field: str   = "embedding"  # default; override in .env if ever needed

    model_config = {
        "env_file": ".env",
        "extra": "forbid",
    }


try:
    settings = Settings()
    logger.info("MongoDB URI: %s", settings.mongodb_uri)
    logger.info("Database: %s", settings.database_name)
    logger.info("Vector index: %s", settings.vector_index_name)
    logger.info("Embedding field: %s", settings.embedding_field)

except ValidationError as err:
    logger.error("Settings validation error: %s", err)
    raise
except Exception as exc:
    logger.error("Error loading settings: %s", exc)
    raise
