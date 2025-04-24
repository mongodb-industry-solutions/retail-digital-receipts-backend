# Base image
FROM python:3.10-slim-buster

ENV DEBIAN_FRONTEND=noninteractive \
    GET_POETRY_IGNORE_DEPRECATION=1

WORKDIR /app

# Install Poetry & dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry==1.8.4 \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-interaction --no-root

# Copy service code
COPY . /app

# Start the worker
CMD ["poetry", "run", "python", "main.py"]