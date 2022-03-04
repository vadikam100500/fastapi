FROM python:3.9.10-slim

WORKDIR /app
COPY ./infra/poetry.lock ./infra/pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install --no-dev
COPY . .
