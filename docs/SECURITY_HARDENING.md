# Security Hardening

## Autenticación y autorización
- Login real (bcrypt + JWT) vs usuarios en BD.
- Roles: `admin`, `notary`, `assistant`, `client`.
- Rutas protegidas por rol (incluye OCR).

## Secretos
- `JWT_SECRET` y `PII_ENC_KEY` obligatorios por entorno (validated).
- Rotación: Secrets Manager / KMS. Soporte para `JWT_SECRET_V2` si lo requieres.

## Archivos y conversión
- Límite tamaño (20MB por defecto). Valida extensión; si requieres, añade `python-magic` para MIME real.
- LibreOffice en contenedor **no root**; ajusta límites de recursos del contenedor.

## Datos y validación
- Validación Pydantic **por plantilla** (schema dinámico).
- S3 con **SSE AES256**; HTTPS para tránsito.

## Observabilidad
- `/metrics` Prometheus.
- Estructura de logs; incluye `job_id` y `template_key`.

## Límites
- Rate limits por ruta/rol (configúralos en `main.py` con SlowAPI).
- Tamaño máximo body.

## Migraciones y cambios
- Alembic baseline incluida; usa CI/CD para `alembic upgrade head` en deploy.
