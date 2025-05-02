.PHONY: build build-invoice build-recommendation clean clean-prod clean-prod-invoice clean-prod-recommendation logs logs-prod logs-invoice logs-recommendation build-prod deploy-prod deploy-invoice-prod deploy-recommendation-prod stop-prod

REGISTRY=retailistregistry-bqfvgkccbfhdhfak.azurecr.io

# -------------------------------
# Local Commands
# -------------------------------

# Build and bring up the services locally
build:
	docker-compose up -d --build

# Clean volumes and unused resources locally
clean:
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# Show logs for the services locally
logs:
	docker-compose logs -f --tail=50

# -------------------------------
# Microservice Specific Commands
# -------------------------------

# Build specific services
build-invoice:
	docker-compose build invoice-ms

build-recommendation:
	docker-compose build recommendation-ms

# -------------------------------
# Production Commands
# -------------------------------

# Clean resources in production
clean-prod:
	az webapp stop --name invoice-ms --resource-group IST-Retail
	az webapp stop --name recommendation-ms --resource-group IST-Retail
	docker system prune -f

# Clean only invoice service resources in production
clean-prod-invoice:
	az webapp stop --name invoice-ms --resource-group IST-Retail
	docker image prune -f --filter "label=service=invoice-ms"

# Clean only recommendation service resources in production
clean-prod-recommendation:
	az webapp stop --name recommendation-ms --resource-group IST-Retail
	docker image prune -f --filter "label=service=recommendation-ms"

# Build and deploy invoice service to production
build-prod-invoice:
	docker build -t $(REGISTRY)/invoice-ms:latest ./services/invoice-ms
	docker push $(REGISTRY)/invoice-ms:latest
	docker run -d --name invoice-ms --rm -p 8000:8000 $(REGISTRY)/invoice-ms:latest

# Build and deploy recommendation service to production
build-prod-recommendation:
	docker build -t $(REGISTRY)/recommendation-ms:latest ./services/recommendation-ms
	docker push $(REGISTRY)/recommendation-ms:latest
	docker run -d --name recommendation-ms --rm -p 8001:8001 $(REGISTRY)/recommendation-ms:latest

# Full production build and deploy process (for both services)
build-prod:
	make build-prod-invoice
	make build-prod-recommendation


# -------------------------------
# Logs Commands for Production
# -------------------------------

# View logs for invoice service in production
logs-prod-invoice:
	az webapp log tail --name invoice-ms --resource-group IST-Retail

# View logs for recommendation service in production
logs-prod-recommendation:
	az webapp log tail --name recommendation-ms --resource-group IST-Retail
