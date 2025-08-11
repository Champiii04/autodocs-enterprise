# Operaciones

## Migraciones (Alembic)
- Baseline incluida en `infra/alembic/versions/0001_baseline.py`.
- Flujo recomendado en CI/CD:
  ```bash
  alembic upgrade head
  ```

## Backups
- PostgreSQL: usa snapshot del proveedor (Railway/Cloud) o `pg_dump` programado.
- S3: activa versionado y políticas de ciclo de vida.

## Métricas
- `GET /metrics` → scrape Prometheus.
- KPI recomendados: latencia de preview, tasa de errores de conversión, tamaño medio de archivos, jobs/minuto.

## Rotación de claves
- Cambia `JWT_SECRET` y `PII_ENC_KEY` usando Secrets Manager/KMS.
- Reinicia servicios para aplicar.

## Tuning
- Worker: aumentar CPU/Mem si hay lotes grandes.
- Colas: `preview` (rápidas) y `batch` (pesadas).
