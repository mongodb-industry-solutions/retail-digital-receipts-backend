# Root Makefile
.PHONY: build start stop clean

build:
	docker-compose up --build -d

start:
	docker-compose start

stop:
	docker-compose stop

clean:
	docker-compose down --rmi all -v

# Optional: Run poetry install for invoice-ms manually
poetry_install_invoice:
	cd services/invoice-ms && poetry install

poetry_install_recommendation:
	cd services/recommendation-ms && poetry install