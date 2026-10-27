# Bóveda: Capacitación KoboToolbox para Arquitectura y Urbanismo
## Levantamiento Georreferenciado Riguroso y Validación de Datos para Estudios Previos de Construcción

> **Nodo:** Prácticas Preprofesionales Finales — Octavo Ciclo (UNL)  
> **Área Receptora:** Facultad / Carrera de Arquitectura Sostenible (Universidad Nacional de Loja)  
> **Directora / Supervisión:** Arq. Alexandra Aguilera Maldonado / Arq. Pablo Araki  
> **Instructores / Autores:** Erick Condoy & Equipo de Prácticas de Economía  
> **Destinatarios:** Estudiantes de Arquitectura (Nivel Inicial e Intermedio)

---

## 📌 Justificación y Rigor Técnico

En los estudios previos de edificación, habilitación de suelo, regeneración urbana y regularización constructiva, un levantamiento de información en campo deficiente o no validado genera rechazo administrativo y graves contingencias de diseño estructural y legal:
1. **Puntos GPS imprecisos:** Coordenadas tomadas con baja señal satelital desplazan los predios fuera de la cartografía municipal o sobre quebradas.
2. **Inconsistencias lógicas:** Registros de edificaciones con "0 pisos" pero con "estructura de hormigón armado", o terrenos declarados con "pendiente nula" en zonas de ladera escarpada.
3. **Falta de evidencia visual estandarizada:** Fotografías desenfocadas, sin escala humana o que no evidencian patologías constructivas reales (fisuras, humedad, asentamientos).
4. **Vacíos de habitabilidad:** Falta de verificación de redes de servicios básicos (acometidas de agua, alcantarillado, tensión eléctrica).

Este curso capacita a los estudiantes de Arquitectura desde **cero absoluto** hasta un nivel de **operador técnico riguroso**, dotándolos del dominio de **KoboToolbox** y **KoboCollect** con lógica de validación **XLSForm** (restricciones lógicas, saltos condicionales, umbrales de precisión GPS y registro fotográfico auditado).

---

## 🗂️ Estructura del Vault

```text
v02-capacitacion-kobotoolbox-arquitectura/
├── README.md                                    # Índice y memoria técnica del taller
├── index.qmd                                    # Cuaderno interactivo / Guía completa web
├── presentacion.qmd                             # Diapositivas oficiales en Quarto Reveal.js
├── presentacion.css                             # Estilos CSS premium para la presentación
├── fichas_xlsform/
│   ├── estructura_xlsform_predial.md            # Esquema tabular de la Ficha Técnica Predial
│   └── guia_validaciones_rigurosas.md           # Catálogo de constraints y relevants
└── guias_estudiantes/
    ├── 01_guia_instalacion_kobocollect.md       # Manual ilustrado móvil Android/iOS y Offline
    ├── 02_protocolo_levantamiento_campo.md      # Estándares de toma fotográfica y GPS en sitio
    ├── 03_exportacion_a_cad_y_qgis.md           # Flujo de datos hacia AutoCAD, QGIS y Revit
    └── 04_tecnicas_investigacion_encuestas_entrevistas_video.md # Guion de entrevistas, aforos y video técnico
```

---

## 🚀 Cómo ejecutar la presentación

Para proyectar las diapositivas en vivo durante la capacitación o generar el archivo HTML autónomo:

```bash
# Renderizar y previsualizar en el navegador
quarto preview presentacion.qmd

# Generar archivo HTML estático para distribución
quarto render presentacion.qmd
```
