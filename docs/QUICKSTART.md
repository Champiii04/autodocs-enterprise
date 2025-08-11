# Quickstart

## 1) Requisitos
- Docker / Docker Compose
- Cuenta en AWS S3 (o compatible) y credenciales
- PostgreSQL y Redis (local/contenerizados o plugins Railway)

## 2) Variables de entorno
Crea `.env` desde `.env.example` (ver abajo). Campos críticos:
- `JWT_SECRET`, `PII_ENC_KEY` **obligatorios**
- `DATABASE_URL`, `REDIS_URL`
- `S3_*` (ACCESS, SECRET, BUCKET, REGION[, ENDPOINT])

## 3) Levantar en local
```bash
docker compose -f infra/docker-compose.yml up --build
# UI: http://localhost:8000/ui
# Login: http://localhost:8000/ui/login  (usa ADMIN_EMAIL/ADMIN_PASSWORD para el seed)
# Métricas: http://localhost:8000/metrics
```

## 4) Flujo de prueba
1. Inicia sesión (admin).
2. En `/ui`, pulsa **Sembrar plantilla de ejemplo**.
3. Ve a `/ui/designer`: edita formulario, presets y previsualiza DOCX.
4. Genera documentos → revisa `/ui/history` y descarga DOCX/PDF.

## 5) CLI útil
- Ver logs del worker: `docker compose logs -f worker`
- Probar endpoints con Postman: `postman/Autodocs.postman_collection.json`
