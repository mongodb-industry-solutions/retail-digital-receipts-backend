# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reminder: Make sure to define the `ENVIRONMENT` environment variable in Docker or your environment.
# The `ENVIRONMENT` variable can have values like "local" or "production".
# In Docker, this variable is defined in the `docker-compose.yml` file as follows:
# environment:
#   - ENVIRONMENT=production  # Or 'local', depending on the environment
# If this variable is not defined, the system will default to using `.env.production`.

# Dynamically select .env file based on the 'ENVIRONMENT' variable
env_file = ".env.local" if os.getenv("ENVIRONMENT") == "local" else ".env.production"

class Settings(BaseSettings):
    mongodb_uri: str
    database_name: str

    class Config:
        env_file = env_file  # Load the appropriate .env file

# Attempt to load the configurations and validate the variables
try:
    settings = Settings()

    # Verify that the variables are loaded correctly
    logger.info("Running with MongoDB URI: %s", settings.mongodb_uri)
    logger.info("Database Name: %s", settings.database_name)

except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise  # Re-raise the error if the necessary configurations cannot be validated

except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    raise  # Re-raise the error if there is any other failure