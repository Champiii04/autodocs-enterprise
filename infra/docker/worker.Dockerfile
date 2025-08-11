FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends libreoffice fonts-dejavu libmagic1 tesseract-ocr && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -U pip && pip install -r requirements.txt
COPY apps/worker /app/apps/worker
COPY apps/api /app/apps/api
ENV PYTHONPATH=/app
CMD ["celery", "-A", "apps.worker.celery_app:celery", "worker", "--loglevel=INFO", "-Q", "preview,default,batch"]

RUN adduser --disabled-password --gecos "" app && chown -R app:app /app
USER app
