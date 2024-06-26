FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH='/'

# TODO: AJUSTAR PARA RODAR SCRIPTS DENTRO DO CONTAINER
COPY ./scripts /scripts
ENV PATH="/scripts:$PATH"

COPY ./poetry.lock /
COPY ./pyproject.toml /

RUN apt-get update -y && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry install \
    && apt-get remove curl -y \
    && chmod -R +x /scripts

COPY ./app /app
WORKDIR /app

CMD ["startup.sh"]