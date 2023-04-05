# Dockerfile
FROM python:3.10-slim as common-base
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir -p /app
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    cron \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --no-input
RUN chown -R root /app
RUN sh -c "python manage.py migrate"
EXPOSE 8080
# ENTRYPOINT ["/app/entrypoint.sh"]