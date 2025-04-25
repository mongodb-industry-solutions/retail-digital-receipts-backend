# Use a lightweight Python 3.10 image
FROM python:3.10-slim

# Install base system dependencies (adjust if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

# Set working directory inside the container
WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml poetry.lock* ./

# Install Poetry and configure it to avoid virtual environments
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Copy the full application code
COPY . .

# Set Python path so 'app.' modules are correctly resolved
ENV PYTHONPATH=/app

# Run the main background processor
CMD ["poetry", "run", "python", "main.py"]
