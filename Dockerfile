FROM python:3.11-slim-bookworm as builder

RUN apt-get update 

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

RUN useradd -m -s /bin/bash appuser

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root $(test "$APP_ENV" == production && echo "--no-dev")

COPY . .

EXPOSE 8080

CMD ["fastapi", "run", "--workers", "4", "--host", "0.0.0.0", "--port", "8080"]




