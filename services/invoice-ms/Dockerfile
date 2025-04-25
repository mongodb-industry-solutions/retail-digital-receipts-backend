# Use a lightweight Python 3.10 image
FROM python:3.10-slim

# Install system dependencies required by WeasyPrint and other libraries
RUN apt-get update && apt-get install -y \
    build-essential \      
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libcairo2 \
    libpq-dev \
    curl && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml poetry.lock* ./

# Install Poetry and configure it to avoid virtual environments
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Copy the application source code into the container
COPY . .

# Expose port 8000 (used by Uvicorn)
EXPOSE 8000

# Start the app using Uvicorn via Poetry
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
