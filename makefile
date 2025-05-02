.PHONY: build clean logs build-invoice build-recommendation clean-prod build-prod

REGISTRY=retailistregistry-bqfvgkccbfhdhfak.azurecr.io
RG=IST-Retail

# Local commands
build:
	@docker-compose up -d --build

clean:
	@docker-compose down --volumes --remove-orphans
	@docker system prune -f

logs:
	@docker-compose logs -f --tail=50

build-invoice:
	@docker-compose build invoice-ms

build-recommendation:
	@docker-compose build recommendation-ms

# Production commands
clean-prod:
	@echo "⏹️  Stopping App Services..."
	@az webapp stop --name invoice-ms --resource-group $(RG)
	@az webapp stop --name recommendation-ms --resource-group $(RG)
	@echo "🧹  Cleaning local Docker resources..."
	@docker image prune -f
	@docker container prune -f

build-prod:
	@echo "🔨 Building invoice-ms image..."
	@docker build -t $(REGISTRY)/invoice-ms:latest ./services/invoice-ms
	@echo "📤 Pushing invoice-ms:latest..."
	@docker push $(REGISTRY)/invoice-ms:latest
	@echo "🚀 Updating invoice-ms on Azure..."
	@az webapp config container set \
	  --name invoice-ms \
	  --resource-group $(RG) \
	  --container-image-name $(REGISTRY)/invoice-ms:latest
	@az webapp restart --name invoice-ms --resource-group $(RG)

	@echo "🔨 Building recommendation-ms image..."
	@docker build -t $(REGISTRY)/recommendation-ms:latest ./services/recommendation-ms
	@echo "📤 Pushing recommendation-ms:latest..."
	@docker push $(REGISTRY)/recommendation-ms:latest
	@echo "🚀 Updating recommendation-ms on Azure..."
	@az webapp config container set \
	  --name recommendation-ms \
	  --resource-group $(RG) \
	  --container-image-name $(REGISTRY)/recommendation-ms:latest
	@az webapp restart --name recommendation-ms --resource-group $(RG)

	@echo "✅ build-prod complete: both services refreshed to :latest"
