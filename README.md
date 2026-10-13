# Prácticas Preprofesionales Finales — Octavo Ciclo (UNL)

Repositorio y nodo soberano de gestión documental, grabaciones, transcripciones, proyectos arquitectónicos e informes para las **Prácticas Preprofesionales Finales** de Octavo Ciclo (Carrera de Economía — Universidad Nacional de Loja), realizadas en el área / carrera de **Arquitectura**.

---

## 🏛️ Información General del Nodo

- **Institución:** Universidad Nacional de Loja (UNL)
- **Carrera de Origen:** Economía (Octavo Ciclo)
- **Área Receptora:** Facultad / Carrera de Arquitectura (UNL)
- **Modalidad:** Prácticas Preprofesionales Laborales / Finales
- **Meta de Horas:** 240 Horas reglamentarias
- **Arquitectura de Nodo:** Nivel 5 — Capital Federated Node

---

## 📂 Estructura del Nodo

```text
03_Practicas_Preprofesionales/
├── .gitignore                      # Exclusiones canónicas (media, raw lake, cachés)
├── Makefile                        # Orquestación de comandos de consola
├── README.md                       # Documentación principal del nodo
├── config/
│   └── node_config.json            # Metadatos del nodo y parámetros de horas
├── bibliography/
│   └── references.bib              # Referencias bibliográficas y normativas
├── guias_formatos/                 # Formatos institucionales UNL y bitácoras tipo
├── informes/                       # Gestión de entregables e hitos formales
│   ├── 00_documentacion_inicial/   # Cartas de aceptación, plan de trabajo, seguro
│   ├── 01_bitacoras_semanales/     # Bitácoras de horas y actividades semanales
│   ├── 02_informes_mensuales/      # Reportes de avance mensual
│   ├── 03_informe_final/           # Informe técnico consolidado final
│   └── 04_evaluaciones_certificados/# Evaluaciones tutor/supervisor y certificados
├── sesiones/                       # Reuniones fechadas YYYY-MM-DD_sesion_XX
│   └── template_sesion/            # Plantilla con grabaciones, transcripciones y notas
├── grabaciones/                    # Archivos brutos (.mp4, .m4a) [excluidos de Git]
├── transcripciones/                # Transcripciones en Markdown (.md) para RAG
├── proyectos_arquitectura/         # Productos técnicos desarrollados en Arquitectura
│   ├── levantamientos_planos/      # Planimetrías, esquemas y planos
│   ├── presupuestos_costos/        # APU, metrados y presupuestos
│   ├── fichas_tecnicas/            # Diagnósticos y especificaciones técnicas
│   └── memorias_descriptivas/      # Informes técnicos de articulación económica
├── docs/                           # Documentación académica y bóvedas
│   ├── syllabus/                   # Sílabo e itinerario de prácticas
│   ├── normativa/                  # Reglamentos de prácticas UNL
│   └── vaults/                     # Bóvedas de evidencias por fases (Quarto)
│       ├── v01-diagnostico-planificacion/
│       ├── v02-ejecucion-actividades/
│       └── v03-cierre-evaluacion/
├── lake/                           # Data Lake federado (RAG / Exocortex)
│   ├── raw/                        # Binarios crudos (excluidos de Git)
│   ├── processed/                  # Datos intermedios procesados
│   └── knowledge/                  # Conocimiento curado indexable
└── scripts/                        # Automatización y scripts de utilidad
    └── auditar_horas.py            # Auditoría y cálculo automático de horas
```

---

## 🎙️ Política de Grabaciones y Prevención de Envenenamiento RAG

1. **Almacenamiento de Grabaciones:**
   - Deposite los audios y videos de reuniones o trabajo de campo en `grabaciones/` o en `sesiones/YYYY-MM-DD_sesion_XX/grabaciones/`.
   - **Garantía Git:** Todos los formatos binarios multimedia (`.mp4`, `.mp3`, `.m4a`, `.wav`, etc.) están estrictamente ignorados en `.gitignore` para no sobrecargar el repositorio.
2. **Transcripciones para RAG:**
   - Convierta las grabaciones a texto Markdown (`.md`) y guárdelas en `transcripciones/` o en la carpeta de sesión respectiva.
   - Solo los archivos `.md` debidamente estructurados son procesados hacia `lake/knowledge/`.

---

## ⏱️ Control y Auditoría de Horas

El nodo cuenta con un script automatizado para auditar el avance de horas registradas en las bitácoras:

```bash
# Vía Makefile:
make audit-hours

# O directamente vía Python:
python scripts/auditar_horas.py
```

---

## 🛠️ Comandos Disponibles (Makefile)

- `make help` : Muestra el listado de comandos disponibles.
- `make status` : Reporta el estado de los directorios `lake/raw`, `lake/knowledge` y `grabaciones`.
- `make audit-hours` : Calcula las horas acumuladas contra la meta institucional de 240 horas.
- `make sync` : Prepara las notas de `lake/knowledge` para ingesta RAG en el Exocortex.
