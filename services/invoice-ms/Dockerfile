# Base image
FROM python:3.10-slim-buster

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    GET_POETRY_IGNORE_DEPRECATION=1

WORKDIR /app

# Install system dependencies for PDF rendering
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

# Copy Poetry files and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry==1.8.4 \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-interaction --no-root

# Copy application code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]