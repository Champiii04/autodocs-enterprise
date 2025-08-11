FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    fonts-dejavu \
    libmagic1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -U pip && pip install -r requirements.txt

COPY apps/api /app/apps/api
COPY apps/worker/renderer /app/apps/worker/renderer
COPY apps/ui /app/apps/ui

ENV PYTHONPATH=/app

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

RUN adduser --disabled-password --gecos "" app && chown -R app:app /app
USER app
