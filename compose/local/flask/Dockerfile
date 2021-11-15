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

# Copy API files
COPY ./trendr /app/trendr

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /app/trendr/requirements.txt
RUN pip install -r /app/trendr/requirements.txt

# Copy start command
COPY ./compose/local/flask/start /app/trendr/start
RUN sed -i 's/\r$//g' /app/trendr/start
RUN chmod +x /app/trendr/start

EXPOSE 5000
ARG FLASK_APP=/app/trendr/app.py
ARG TWITTER_CONSUMER_KEY
ARG TWITTER_CONSUMER_SECRET
ARG ETHPLORER_KEY
ARG FINNHUB_KEY
ARG DATABASE_URL
ARG SQLALCHEMY_DATABASE_URI

ENTRYPOINT ["/app/trendr/start"]