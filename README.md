# Tramita Ya — Autodocs Enterprise (Secure)

Plataforma de automatización documental tipo DocsAutomator, endurecida para producción:
- **Diseñador visual** con presets Perú, validación en vivo y condicionales.
- **Render asíncrono** (Celery) y multiformato (DOCX/PDF/ODT/HTML).
- **S3** con cifrado en reposo, **Redis cache** para previews.
- **RBAC** y **login real** (bcrypt + JWT).
- **Historial** con descargas directas, **API keys** por proyecto, **OCR**.
- **Observabilidad**: `/metrics` Prometheus.

> Documentación completa en `docs/`:

- `docs/QUICKSTART.md` (arranque rápido)
- `docs/ARCHITECTURE.md` (componentes y flujos)
- `docs/DEPLOY_RAILWAY.md` (staging/producción)
- `docs/SECURITY_HARDENING.md` (endurecimiento y checklist)
- `docs/API_REFERENCE.md` (referencia de endpoints)
- `docs/OPERATIONS.md` (migraciones, backups, métricas, rotación de secretos)
- `docs/FORM_TEMPLATES.md` (plantillas, condicionales, relleno ====)
- `docs/TROUBLESHOOTING.md` (errores comunes y soluciones)

Incluye `postman/Autodocs.postman_collection.json` para pruebas.
