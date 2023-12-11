FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/opt/poetry, POETRY_VIRTUALENVS_CREATE=false, POETRY_VERSION=1.3.0

# Install poetry
RUN python3 -m pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev --no-root

COPY /src /app/src

RUN poetry install --no-dev --only-root

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
