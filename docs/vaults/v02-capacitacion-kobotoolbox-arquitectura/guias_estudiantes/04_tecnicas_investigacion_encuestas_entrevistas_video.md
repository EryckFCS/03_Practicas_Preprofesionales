# Técnicas de Investigación en Territorio para Arquitectura & Urbanismo
## Guía Metodológica: Encuestas Cuantitativas, Entrevistas Semiestructuradas y Evidencia Multimedia (Video/Audio)

> **Proyecto:** Levantamiento Integral y Diagnóstico Territorial — Barrio El Capulí (Loja)  
> **Área Receptora:** Carrera de Arquitectura Sostenible (UNL)  
> **Supervisión Técnica:** Arq. Alexandra Aguilera Maldonado / Arq. Pablo Araki  
> **Elaboración:** Erick Condoy & Equipo de Prácticas de Economía

---

## 1. Justificación Metodológica: La Triangulación Territorial

En los estudios previos para edificación y regularización urbana, la información debe ser contrastada desde tres fuentes independientes para evitar falsos positivos y rechazos periciales:

```text
                        ┌──────────────────────────────┐
                        │   1. TÉCNICA CUALITATIVA     │
                        │   Entrevista a profundidad   │
                        │   (Percepción y memoria)     │
                        └──────────────┬───────────────┘
                                       ▲
                                      / \
                                     /   \
                                    /     \
                                   ▼       ▼
    ┌─────────────────────────────┐         ┌─────────────────────────────┐
    │   2. TÉCNICA CUANTITATIVA   │         │    3. EVIDENCIA PERICIAL    │
    │   Encuesta predial cerrada  │◄───────►│    Fotografía técnica,      │
    │   (Cifras, materiales, NBI) │         │    video dinámico y GPS     │
    └─────────────────────────────┘         └─────────────────────────────┘
```

---

## 2. Técnica 1: Encuesta Cuantitativa Estructurada

### Características:
- **Cero ambigüedad:** Cada pregunta tiene opciones cerradas (`select_one`, `select_multiple`) o valores numéricos discretos (`integer`, `decimal`).
- **Alineación con el Censo INEC:** Las preguntas de servicios básicos (acometida de agua, eliminación de excretas, energía eléctrica) y materiales de cubierta/muros utilizan la nomenclatura oficial para poder contrastar con los datos censales REDATAM del sector.

### Recomendaciones en Campo:
1. Nunca formule preguntas inductivas (ejemplo erróneo: *"¿Verdad que este lote tiene agua potable?"* $\rightarrow$ correcto: *"¿De dónde proviene el agua que consume este hogar?"*).
2. Inspeccione con sus propios ojos la presencia de medidores de agua o luz antes de marcar la respuesta.

---

## 3. Técnica 2: Entrevista Semiestructurada a Actores Clave

### A quién entrevistar:
- Presidentes de la Junta Barrial o comités de pro-mejoras.
- Moradores de mayor antigüedad (más de 15 a 20 años residiendo en el sector).
- Constructores o maestros mayores de obra locales.

### Guion Modelo de Preguntas Abiertas (Grabación de Audio en Kobo):
1. **Historia y Transformación del Barrio:**  
   *«¿Cómo se originó el asentamiento en este sector y cuáles han sido los principales cambios en los últimos diez años?»*
2. **Memoria de Riesgos Geológicos e Hidrológicos:**  
   *«¿En qué épocas de invierno se han presentado crecidas de la quebrada o deslizamientos de tierra en las laderas cercanas? ¿Hasta dónde llegó la afectación?»*
3. **Déficit de Espacio Público y Equipamiento:**  
   *«¿Qué espacios hacen falta con mayor urgencia para los niños, jóvenes y adultos mayores (parques, canchas, casa comunal, paradas de bus)?»*
4. **Conflictos de Tenencia y Linderación:**  
   *«¿Existen problemas frecuentes entre vecinos por los linderos de los lotes o la falta de escrituras?»*

### Reglas de Grabación de Audio:
- Duración recomendada: **2 a 4 minutos por entrevista**.
- Pida autorización explícita antes de presionar el botón de grabar en KoboCollect.
- Grabe en un espacio protegido del viento o del ruido de motores para garantizar la inteligibilidad de la voz.

---

## 4. Técnica 3: Video Técnico y Registro Dinámico

### Cuándo el video es insustituible por una fotografía:
- **Flujos hidrológicos activos:** Movimiento de agua en cauces naturales, escorrentías sobre calzadas y taponamiento de alcantarillas.
- **Topografía compleja:** Paneo que expone el ángulo real de corte de un talud o ladera escarpada.
- **Patologías estructurales en serie:** Recorrido continuo a lo largo de una grieta en un muro de contención o viga.
- **Aforo perceptual:** Movimiento de peatones y transporte público en intersecciones críticas.

### Especificaciones Técnicas del Video en KoboCollect:
- **Resolución:** Configurar la cámara en **720p (HD)** a 30 fps.
- **Duración Máxima:** **15 a 25 segundos**.
- **Movimiento:** Paneo horizontal lento y uniforme (velocidad angular baja). Prohibido correr o hacer paneos rápidos que causen desenfoque.
- **Audio ambiental:** Mantener silencio durante la grabación para captar el sonido del entorno (tráfico, quebrada, viento).

---

## 5. Formato de Consentimiento Informado Verbal

Antes de iniciar cualquier entrevista, fotografía o grabación en KoboCollect, el encuestador debe leer en voz alta:

> *«Buenos días/tardes. Somos estudiantes de la Carrera de Arquitectura Sostenible de la Universidad Nacional de Loja. Estamos realizando un levantamiento técnico de información para el diagnóstico urbano y la mitigación de riesgos del barrio El Capulí. Los datos, audios e imágenes que nos brinde serán tratados con estricta confidencialidad con fines académicos y de planificación técnica. ¿Está de acuerdo en participar voluntariamente en esta encuesta y permitir el registro fotográfico/sonoro de su inmueble?»*

En KoboCollect se registra obligatoriamente:  
`acepta_participar` $\rightarrow$ `si` / `no`.  
Si la persona responde `no`, se guarda el formulario únicamente con la coordenada del espacio público exterior y se finaliza la visita cordialmente.
