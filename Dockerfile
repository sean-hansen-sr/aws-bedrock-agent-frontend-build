FROM python:3.13-slim

ARG APP_ENV
ARG APP_AGENT_BASE_URL

ENV APP_ENV=$APP_ENV
ENV AGENT_BASE_URL=$APP_AGENT_BASE_URL

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8080", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]