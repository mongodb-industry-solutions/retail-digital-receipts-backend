FROM python:3.10.18-slim

# Install base system dependencies (adjust if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Clean up to reduce image size
RUN apt-get remove --purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*  # Remove apt cache

COPY . .

# Set Python path so 'app.' modules are correctly resolved
ENV PYTHONPATH=/app

# Puerto estándar para Kanopy
ENV PORT=8080
EXPOSE 8080

CMD ["poetry", "run", "python", "main.py"]