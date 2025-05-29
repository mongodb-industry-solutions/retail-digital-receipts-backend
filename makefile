# -------------------------------
# 📦 Variables (Customize below)
# -------------------------------

# Azure Container Registry (replace with your own ACR login name)
REGISTRY=retailistregistry-bqfvgkccbfhdhfak.azurecr.io

# Azure Resource Group where your App Services are deployed
RG=IST-Retail

# -------------------------------
# 🔨 Local Development Commands
# -------------------------------

# Build and start all services using Docker Compose
build:
	@docker-compose up -d --build

# Fully stop and remove containers, volumes, and orphans
# ⚠️ WARNING: This will delete local data stored in volumes
clean:
	@echo "💥 Cleaning local environment..."
	@docker-compose down --volumes --remove-orphans
	@docker system prune -f

# View logs from all running local containers
logs:
	@docker-compose logs -f --tail=50

# Build only the invoice microservice locally
build-invoice:
	@docker-compose build invoice-ms

# Build only the recommendation microservice locally
build-recommendation:
	@docker-compose build recommendation-ms

# Stop only the invoice microservice locally
stop-invoice:
	@docker-compose stop invoice-ms

# Stop only the recommendation microservice locally
stop-recommendation:
	@docker-compose stop recommendation-ms

# -------------------------------
# 🚀 Production Commands (Azure)
# -------------------------------

# Stop all Azure App Services
stop-prod:
	@echo "⏹️  Stopping App Services..."
	@az webapp stop --name invoice-ms --resource-group $(RG)
	@az webapp stop --name recommendation-ms --resource-group $(RG)

# Stop only invoice-ms in Azure
stop-invoice-prod:
	@az webapp stop --name invoice-ms --resource-group $(RG)

# Stop only recommendation-ms in Azure
stop-recommendation-prod:
	@az webapp stop --name recommendation-ms --resource-group $(RG)

# Deploy both microservices: build, push and restart in Azure
deploy-prod:
	@echo "🔨 Creating buildx builder (if not exists)..."
	@docker buildx create --name retailist-builder --use || true
	@echo "🔨 Building invoice-ms image for linux/amd64..."
	@docker buildx build --platform linux/amd64 -t $(REGISTRY)/invoice-ms:latest ./services/invoice-ms --push
	@echo "🚀 Deploying invoice-ms to Azure..."
	@az webapp config container set \
		--name invoice-ms \
		--resource-group $(RG) \
		--container-image-name $(REGISTRY)/invoice-ms:latest
	@az webapp restart --name invoice-ms --resource-group $(RG)
	@echo "🔨 Building recommendation-ms image for linux/amd64..."
	@docker buildx build --platform linux/amd64 -t $(REGISTRY)/recommendation-ms:latest ./services/recommendation-ms --push
	@echo "🚀 Deploying recommendation-ms to Azure..."
	@az webapp config container set \
		--name recommendation-ms \
		--resource-group $(RG) \
		--container-image-name $(REGISTRY)/recommendation-ms:latest
	@az webapp restart --name recommendation-ms --resource-group $(RG)
	@echo "✅ deploy-prod complete: both services deployed to Azure"

# Deploy only invoice-ms to Azure
deploy-invoice-prod:
	@echo "🔨 Building invoice-ms image for linux/amd64..."
	@docker buildx build --platform linux/amd64 -t $(REGISTRY)/invoice-ms:latest ./services/invoice-ms --push
	@echo "🚀 Deploying invoice-ms to Azure..."
	@az webapp config container set \
		--name invoice-ms \
		--resource-group $(RG) \
		--container-image-name $(REGISTRY)/invoice-ms:latest
	@az webapp restart --name invoice-ms --resource-group $(RG)

# Deploy only recommendation-ms to Azure
deploy-recommendation-prod:
	@echo "🔨 Building recommendation-ms image for linux/amd64..."
	@docker buildx build --platform linux/amd64 -t $(REGISTRY)/recommendation-ms:latest ./services/recommendation-ms --push
	@echo "🚀 Deploying recommendation-ms to Azure..."
	@az webapp config container set \
		--name recommendation-ms \
		--resource-group $(RG) \
		--container-image-name $(REGISTRY)/recommendation-ms:latest
	@az webapp restart --name recommendation-ms --resource-group $(RG)

# -------------------------------
# ⚙️ Declare all targets as phony
# -------------------------------
.PHONY: build clean logs \
	build-invoice build-recommendation \
	stop-invoice stop-recommendation \
	stop-prod stop-invoice-prod stop-recommendation-prod \
	deploy-prod deploy-invoice-prod deploy-recommendation-prod \
	logs-prod