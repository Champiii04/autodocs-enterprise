# Deploy en Railway

## 1) Repo y servicios
- Sube el **contenido** del proyecto a GitHub.
- Railway → New Project → Deploy from GitHub.
- Detecta `railway.json`: servicios `api` y `worker` (Dockerfile).

## 2) Plugins
- PostgreSQL
- Redis

## 3) Variables (en **api** y **worker**)
```
DATABASE_URL=<postgres-railway-url>
REDIS_URL=<redis-railway-url>
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}

S3_ACCESS_KEY=...
S3_SECRET_KEY=...
S3_BUCKET=tramitaya-docs-staging
S3_REGION=us-east-1
S3_ENDPOINT=   # vacío para AWS nativo

JWT_SECRET=<largo y aleatorio>
PII_ENC_KEY=<largo y aleatorio>

# Seed admin (opcional en 1er arranque)
ADMIN_EMAIL=admin@tramita-ya.com
ADMIN_PASSWORD=<segura>
ADMIN_ROLE=admin
```

## 4) Endpoints útiles
- UI: `/ui`, login: `/ui/login`
- Health: `/healthz`
- Métricas: `/metrics`

## 5) Observabilidad y escalamientos
- Monitorea `/metrics` (Prometheus/Grafana).
- Ajusta plan de Railway según lote/volumen (CPU/Mem para worker).
