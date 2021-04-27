FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry==1.1.5 && \
    poetry export --without-hashes -f requirements.txt -n -o requirements.txt && \
    pip uninstall --yes poetry && \
    pip install -r requirements.txt
