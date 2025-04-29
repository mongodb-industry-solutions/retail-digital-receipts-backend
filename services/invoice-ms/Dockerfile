# Use a lightweight Python 3.10 base image
FROM python:3.10-slim

# Install system dependencies required by WeasyPrint and others
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

# --- OPTIONAL: Install Azure CLI for local development ---
# This is required for AzureCliCredential to work inside the container during local development
# Do NOT rely on this in production (use Managed Identity instead)
RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" \
        > /etc/apt/sources.list.d/azure-cli.list && \
    apt-get update && \
    apt-get install -y azure-cli && \
    rm -f microsoft.gpg && \
    apt-get clean
# --------------------------------------------------------

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definitions (Poetry files)
COPY pyproject.toml poetry.lock* ./

# Install Poetry and configure it to not create virtual environments
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Copy the application source code into the container
COPY . .

# Expose port 8000 for Uvicorn server
EXPOSE 8000

# Start the FastAPI application with Uvicorn through Poetry
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Notes ---
# In production (e.g. Azure App Service), authentication should use Managed Identity.
# In local development, you can authenticate via `az login` on your host machine,
# and mount your ~/.azure config into the container like this (in docker-compose file):
# volumes:
#   - $HOME/.azure:/root/.azure
