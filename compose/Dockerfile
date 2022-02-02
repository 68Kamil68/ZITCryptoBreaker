FROM python:3.10.1-slim-buster

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

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN chmod +x /start

COPY ./compose/celery/worker/start /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/celery/beat/start /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/celery/flower/start /start-flower
RUN chmod +x /start-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
