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

# OPTIONAL: Enable this for Azure CLI inside container (for local dev only)
# RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
#     install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ && \
#     echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" \
#         > /etc/apt/sources.list.d/azure-cli.list && \
#     apt-get update && \
#     apt-get install -y azure-cli && \
#     rm -f microsoft.gpg && \
#     apt-get clean

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]