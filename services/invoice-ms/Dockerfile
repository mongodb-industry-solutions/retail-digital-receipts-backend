FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libcairo2 \
    libpq-dev \
    curl \
    gnupg \
    lsb-release && \
    apt-get clean

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Clean up to reduce image size
RUN apt-get remove --purge -y build-essential libpq-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*  # Remove apt cache

COPY . .

# Puerto estándar para Kanopy
ENV PORT=8080
EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]