# Troubleshooting

## 502/504 al previsualizar
- Verifica Redis y que `REDIS_URL` esté correcto.
- Revisa logs de API por errores de validación (422).

## 500 al convertir a PDF/ODT/HTML
- LibreOffice puede fallar con documentos dañados.
- Ver logs del **worker**. Si es `.doc`, intenta abrir en una suite y re-guardar como `.docx`.

## Previews inconsistentes
- Cache Redis dura 5 min; cambia un campo del JSON para forzar re-render.
- Si re-subiste la plantilla, vuelve a crear el formulario.

## “Token inválido”
- JWT expirado o `JWT_SECRET` distinto en api y worker. Asegura mismas variables.

## OCR no funciona
- Verifica tesseract instalado (está en Docker) y que subes PNG/JPG legibles.
