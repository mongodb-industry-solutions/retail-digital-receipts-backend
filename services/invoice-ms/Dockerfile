# Dockerfile for invoice-ms

# Use the official Python image (version 3.10-slim) as the base image
FROM python:3.10-slim-buster

# Set the environment variable to avoid deprecation warnings with Poetry
ENV GET_POETRY_IGNORE_DEPRECATION=1

# Set the working directory inside the container
WORKDIR /app

# Step 1: Copy the pyproject.toml and poetry.lock files from the root of invoice-ms
# These files define the project dependencies and versions
COPY invoice-ms/pyproject.toml invoice-ms/poetry.lock /app/

# Step 2: Install Poetry (dependency manager)
RUN pip install poetry==1.8.4

# Step 3: Configure Poetry to install dependencies in the project directory
RUN poetry config virtualenvs.in-project true

# Step 4: Install project dependencies from poetry.lock
RUN poetry install --no-interaction -v --no-cache --no-root

# Step 5: Copy the rest of the application code into the container
COPY ./invoice-ms /app/

# Step 6: Copy .env.local file from the root of invoice-ms directory to the container
COPY invoice-ms/.env.local /app/.env.local

# Step 7: Expose port 8000 to make the service available externally
EXPOSE 8000

# Step 8: Run the FastAPI app using Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
