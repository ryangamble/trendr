FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy neccessary project files
COPY ./.env/.env_apis /app/.env/.env_apis
COPY ./.env/.env_dev /app/.env/.env_dev
COPY ./.env/.env_mail_secrets /app/.env/.env_mail_secrets
COPY ./migrations /app/migrations
COPY ./trendr /app/trendr

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy start command
COPY ./compose/local/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/flask/celery/worker/general/start /start-celeryworker-general
RUN sed -i 's/\r$//g' /start-celeryworker-general
RUN chmod +x /start-celeryworker-general

COPY ./compose/local/flask/celery/worker/social/start /start-celeryworker-social
RUN sed -i 's/\r$//g' /start-celeryworker-social
RUN chmod +x /start-celeryworker-social

COPY ./compose/local/flask/celery/worker/sentiment/start /start-celeryworker-sentiment
RUN sed -i 's/\r$//g' /start-celeryworker-sentiment
RUN chmod +x /start-celeryworker-sentiment

COPY ./compose/local/flask/celery/worker/search/start /start-celeryworker-search
RUN sed -i 's/\r$//g' /start-celeryworker-search
RUN chmod +x /start-celeryworker-search

COPY ./compose/local/flask/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/flask/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /app