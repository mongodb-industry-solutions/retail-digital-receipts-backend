.PHONY: build clean logs restart

# Start and build all services
build:
	docker-compose up -d --build

# Stop and remove everything: containers, volumes, and orphans
clean:
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# Show live logs
logs:
	docker-compose logs -f --tail=50

# Rebuild and restart everything
restart:
	make clean
	make build
