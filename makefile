.PHONY: build clean logs

# Build and start all services in detached mode
build:
	docker-compose up -d --build

# Stop and remove all services, volumes, and orphan containers
clean:
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# Show the last 50 log lines and follow logs in real time
logs:
	docker-compose logs -f --tail=50

# Notes:
# - 'make build' builds the Docker images and starts containers in the background.
# - 'make logs' displays the latest 50 lines of logs and follows the output live.
# - 'make clean' stops all running services, removes volumes and orphan containers, and prunes unused Docker resources.
# - This Makefile is optimized for local development using Azure CLI authentication outside containers.
# - In production (Azure App Service), authentication is handled via Managed Identity automatically.
