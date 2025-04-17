# Use the official Python image (version 3.10-slim) as the base image
FROM python:3.10-slim-buster

# Set environment variable to avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
ENV GET_POETRY_IGNORE_DEPRECATION=1

# Set working directory
WORKDIR /app

# 👉 Install system dependencies required for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Step 1: Copy Poetry files first to install dependencies separately
COPY invoice-ms/pyproject.toml invoice-ms/poetry.lock /app/

# Step 2: Install Poetry
RUN pip install poetry==1.8.4

# Step 3: Configure Poetry to install in the project directory
RUN poetry config virtualenvs.in-project true

# Step 4: Install project dependencies
RUN poetry install --no-interaction --no-root

# Step 5: Copy application code
COPY ./invoice-ms /app/

# Step 6: Copy environment variables
COPY invoice-ms/.env.local /app/.env.local

# Step 7: Expose port for FastAPI
EXPOSE 8000

# Step 8: Run FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
