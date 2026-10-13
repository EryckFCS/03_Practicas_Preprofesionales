# Sesiones y Reuniones de Prácticas Preprofesionales

Este directorio permite estructurar reuniones semanales o sesiones de tutoría/supervisión por carpetas fechadas e independientes.

## Convención de Nomenclatura:

Cada sesión sigue el estándar:
`YYYY-MM-DD_sesion_XX/` (Ejemplo: `2026-10-15_sesion_01/`)

## Estructura Interna por Sesión:

```
YYYY-MM-DD_sesion_XX/
├── grabaciones/      <- Archivos brutos (.mp4, .m4a) [excluidos de Git]
├── transcripciones/  <- Texto depurado en Markdown (.md)
└── notas/            <- Apuntes rápidos, acuerdos y minutas (.md)
```

Para crear una nueva sesión, copie la plantilla base ubicada en `sesiones/template_sesion/`.
