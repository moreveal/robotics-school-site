FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

RUN apt-get update && apt-get install -y gettext

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
