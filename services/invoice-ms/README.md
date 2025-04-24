# 🧾 invoice-ms

Handles creation, enrichment, and rendering of invoices from new orders.  
Part of the retail demo system using MongoDB Change Streams, Azure Functions, and Clean Architecture.

---

## 🔍 What it does

- Listens for new order inserts via MongoDB Change Streams
- Creates a new invoice based on the order
- Enriches it using an external Azure Function (mocked for demo)
- Stores the invoice in MongoDB
- Renders a PDF/image version of the invoice (on demand)
- Uploads the rendered file to Azure Blob Storage
- Provides an API to retrieve the invoice file

> If the invoice hasn't been rendered yet, the endpoint will trigger the rendering and return the result.  
> The rendered file includes **recommendations inserted by `recommendation-ms`** via an Atlas Trigger.

---

## 🏗️ Architecture Overview

### 1. Event-Driven Invoice Creation

![Invoice Creation Flow](../../docs/images/create-invoice-architecture-ecosystem.png)

- Change Stream detects `orders.insert`
- `invoice-ms` creates and saves invoice
- Calls Azure Function to enrich data (if available)

### 2. PDF Rendering On-Demand

![Invoice Rendering Flow](../../docs/images/get-invoice-architecture-ecosystem.png)

- Endpoint `/invoices/{invoice_id}/file`
- If rendered file exists → returns it
- Else → triggers generation, uploads to Blob Storage, and returns link

---

## ⚙️ Setup Instructions

> 👉 If you're looking to run the full system (including `invoice-ms`, Azure Functions, and shared MongoDB setup), head to the [main project README](../../README.md) for a complete guide.

## 🔧 Prerequisites

- Python 3.10 (recommended)
- Poetry installed ([guide](https://python-poetry.org/docs/#installation))
- Access to a MongoDB Atlas cluster
- Azure Storage credentials (see `.env.example`)
- Clone the repo and navigate to `services/invoice-ms`
- Create your `.env.local` file (see `.env.example`)

## ▶️ Setup (Local, No Docker)


3. Run the following:

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start the FastAPI server
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```
## 🐳 Setup with Docker

You can run `invoice-ms` in an isolated container using Docker.

### 🔧 1. Create the environment config

Make sure you have a valid `.env.local` file at the root of `invoice-ms`.  
Use `.env.example` as a template.

```bash
cp .env.example .env.local
```
### 🛠️ 2. Build the Docker image

```bash
docker build -t invoice-ms .
```

This will:

Use the official Python 3.10 slim image

Install dependencies via Poetry

Set up FastAPI and your app code

Expose port 8000

### ▶️ 3. Run the container

```bash
docker run --env-file .env.local -p 8000:8000 invoice-ms
```
Your service should now be available at:
http://localhost:8000

### 📎 Notes
Make sure your MongoDB instance and Azure environment variables are reachable from the container.

Azure credentials (for Blob upload) must be correctly set in .env.local.