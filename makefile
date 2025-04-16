# Build the Docker image and start the containers in detached mode
build:
	docker-compose up --build -d

# Start all services defined in docker-compose (useful after they are stopped)
start:
	docker-compose start

# Stop the running containers without removing them
stop:
	docker-compose stop

# Clean up containers, networks, volumes, and images
clean:
	docker-compose down --rmi all -v

# Install Poetry using pipx
install_poetry:
	brew install pipx
	pipx ensurepath
	pipx install poetry==1.8.4

# Configure Poetry to create the virtual environment within the project directory
poetry_start:
	cd services/invoice-ms && poetry config virtualenvs.in-project true

# Install the dependencies of the invoice-ms microservice using Poetry
poetry_install:
	cd services/invoice-ms && poetry install --no-interaction -v --no-cache --no-root

# Update Poetry dependencies for the invoice-ms microservice
poetry_update:
	cd services/invoice-ms && poetry update

# Health check: Verify if the invoice-ms service is running correctly
healthcheck:
	curl --fail http://localhost:8000/health || exit 1

# Rebuild and restart the containers
rebuild:
	make down
	make build
	make start