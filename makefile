.PHONY: build build-invoice build-recommendation clean logs build-prod deploy-prod deploy-invoice-prod deploy-recommendation-prod stop-prod logs-invoice-prod logs-recommendation-prod

# Replace with your Azure Container Registry
REGISTRY=retailistregistry-bqfvgkccbfhdhfak.azurecr.io

build:
	docker-compose up -d --build

clean:
	docker-compose down --volumes --remove-orphans
	docker system prune -f

logs:
	docker-compose logs -f --tail=50

build-invoice:
	docker-compose build invoice-ms

build-recommendation:
	docker-compose build recommendation-ms

build-prod:
	docker build -t $(REGISTRY)/invoice-ms:latest ./services/invoice-ms
	docker push $(REGISTRY)/invoice-ms:latest
	docker build -t $(REGISTRY)/recommendation-ms:latest ./services/recommendation-ms
	docker push $(REGISTRY)/recommendation-ms:latest

deploy-invoice-prod:
	docker build -t $(REGISTRY)/invoice-ms:latest ./services/invoice-ms
	docker push $(REGISTRY)/invoice-ms:latest

deploy-recommendation-prod:
	docker build -t $(REGISTRY)/recommendation-ms:latest ./services/recommendation-ms
	docker push $(REGISTRY)/recommendation-ms:latest

deploy-prod:
	make deploy-invoice-prod
	make deploy-recommendation-prod

stop-prod:
	az webapp stop --name invoice-ms --resource-group ISTRetail
	az webapp stop --name recommendation-ms --resource-group ISTRetail

# Tail logs from the Azure App Services
logs-invoice-prod:
	az webapp log tail --name invoice-ms --resource-group ISTRetail

logs-recommendation-prod:
	az webapp log tail --name recommendation-ms --resource-group ISTRetail
