# API Reference

## Auth
- `POST /auth/login` → {email, password} → JWT (Bearer).

## Templates & Forms
- `POST /v1/templates/autoform` (JWT: admin/notary/assistant) → sube `.doc/.docx` → detecta variables y crea formulario.
- `GET /v1/forms/{template_key}` → obtiene schema.
- `PUT /v1/forms/{id}` (JWT: admin/notary/assistant) → actualiza schema.

## Preview & Generate
- `POST /v1/preview/{template_key}` (JWT) → valida datos y devuelve DOCX (cache Redis).
- `POST /v1/generate/{template_key}` (JWT) → encola render (DOCX/PDF/ODT/HTML).
- `GET /v1/jobs/{job_id}` (JWT) → estado y URLs presignadas.

## Batch
- `POST /v1/generate/{template_key}/batch` (JWT: admin/notary) → CSV → encola por fila.

## History
- `GET /v1/history/search?status=&start_id=&end_id=&limit=` (JWT) → lista con descargas directas.
- `GET /v1/history/recent` (JWT).

## API Keys (admin)
- `POST /v1/apikeys/projects` {name} → crea proyecto
- `POST /v1/apikeys/projects/{project_id}/keys` → crea API key
- `GET /v1/apikeys/projects`
- `GET /v1/apikeys/projects/{id}/keys`

## External
- `POST /v1/external/generate/{template_key}` (X-API-Key) → igual a generate pero para terceros.

## OCR
- `POST /v1/ocr/scan` (JWT: admin/notary/assistant) → extrae texto de PNG/JPG.
