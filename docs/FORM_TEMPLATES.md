# Plantillas y formularios

## Placeholders
- Usa `{{ CAMPO }}` en el DOCX para variables.
- Autoform detecta placeholders y genera un formulario base.

## Campos inteligentes
- `type`: text, number, date, select, textarea, email
- `mask.regex`: validación (DNI `^\d{8}$`, RUC `^\d{11}$`)
- `transform: "uppercase"`: convierte a mayúsculas antes del render.
- `show_if`: condicional (ej. mostrar `ALCANCE` si `PODER_TIPO == "ESPECIAL"`).

## Relleno de líneas `====`
- En plantilla: `{{ NOMBRE|pad(60,'=') }}` → completa a un ancho fijo con `=`.
- Post-proceso: cualquier secuencia `===` o más se estira a ancho uniforme (config por código en `expand_equals_lines`).

## Tips DOCX
- Mantén fuentes y estilos consistentes en el .docx base.
- Evita saltos de línea “raros” dentro de `{{ }}` (mejor en una sola línea).
