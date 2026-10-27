# Guía de Validaciones Rigurosas en KoboToolbox para Estudios de Construcción

> **Objetivo:** Garantizar que ningún dato recolectado en campo por los estudiantes pueda ser objetado o rechazado por peritos municipales, directores de proyecto o entes de licenciamiento constructivo.

---

## 1. El Costo de un Dato No Validado en Arquitectura

En la práctica profesional de la arquitectura y la ingeniería civil, los errores de campo generan pérdidas económicas, retrasos en la obtención de permisos y rediseños costosos:

1. **Error de Linderos y Retiros:** Si el estudiante levanta un frente de lote erróneo o una coordenada GPS desplazada 10 metros, el proyecto arquitectónico invade servidumbres de paso o el retiro frontal reglamentario.
2. **Falsos Positivos de Cimentación:** Reportar suelo "apto y plano" en una zona con pendientes del 28% conduce a diseños estructurales subdimensionados que fallan ante movimientos de tierras o lluvias torrenciales.
3. **Discrepancias Catastrales:** Un código de predio mal tipiado (`L-04` en lugar de `M02-L04`) hace imposible cruzar los datos de campo con la base de datos municipal o las escrituras públicas.

---

## 2. Catálogo de Reglas y Expresiones de Validación (`constraint`)

### A. Control de Precisión del Punto GPS (`geopoint`)
- **Problema:** Los teléfonos móviles con poca batería o bajo árboles capturan coordenadas con errores de hasta 40 metros.
- **Solución técnica en KoboCollect:**  
  Configurar en la aplicación el **Umbral de Precisión GPS** en 5 metros.
- **En la hoja XLSForm:**  
  Para campos de cálculo o alerta:
  ```xlsform
  constraint: . <= 5.0
  constraint_message: "Error de GPS inaceptable (> 5m). Desplácese a un punto despejado y espere la fijación de satélites."
  ```

### B. Validación de Dimensiones Físicas y Rangos Coherentes
- **Frente de Lote:**
  - Expresión: `. >= 5.0 and . <= 80.0`
  - Evita que el encuestador ingrese por error `0.6` (en centímetros en vez de metros) o `500` por exceso de tipeo.
- **Número de Pisos:**
  - Expresión: `. >= 1 and . <= 6`
  - Ninguna vivienda de tipología barrial común supera los 6 niveles sin ascensor o cálculo especial.
- **Año Estimado de Construcción:**
  - Expresión: `. >= 1950 and . <= 2026`
  - Evita años absurdos como `2062` o `120`.

### C. Validación de Formato de Códigos (Expresiones Regulares - `regex`)
Para evitar que cada estudiante invente su propio formato de registro:
- **Código de Ficha:**
  - Expresión: `regex(., '^ARQ-[0-9]{3}$')`
  - Obliga a escribir exactamente: `ARQ-001`, `ARQ-015`, etc.
- **Cédula de Propietario / Informante (Ecuador):**
  - Expresión: `regex(., '^[0-9]{10}$')`
  - Exige exactamente 10 dígitos numéricos.

---

## 3. Coherencia Cruzada entre Preguntas

Una de las causas más frecuentes de rechazo de informes es la **incoherencia interna** entre dos respuestas del mismo predio.

### Regla 1: Baldío vs. Características Constructivas
- Si en `estado_ocupacion` se selecciona `baldio`, **todas las preguntas de la edificación deben ocultarse automáticamente** usando `relevant`:
  ```xlsform
  relevant: ${estado_ocupacion} != 'baldio'
  ```
- *Riesgo evitado:* Que un predio vacío tenga registradas características de "muros de ladrillo" y "cubierta de teja".

### Regla 2: Daño Estructural vs. Severidad y Evidencia
- La pregunta sobre el tipo de patología (`patologias`) y la fotografía de la falla (`foto_dano`) **solo deben activarse si previamente se declaró la existencia de daño**:
  ```xlsform
  relevant: ${presenta_dano} = 'si'
  ```
- Además, si se marca que existe daño, la foto debe tener `required = yes`. No se admite reporte de fisura sin evidencia gráfica.

---

## 4. Estándar de Auditoría en Servidor

Para que el informe sea aprobado por la Directora de Carrera o el Supervisor Técnico:

1. **Revisión Diaria en KoboToolbox:**
   - Acceder al módulo **"Datos" $\rightarrow$ "Tabla"**.
   - Filtrar por la columna de **Precisión GPS**. Cualquier registro con precisión mayor a 6 metros se marca con estado de validación: **"Rechazado"** (`Not Approved`).
2. **Inspección de Fotografías:**
   - Comprobar que la foto de fachada permita identificar el número de pisos y el tipo de cubierta declarado en el formulario.
3. **Control de Duplicados:**
   - Verificar que no existan dos registros con el mismo código de manzana y lote.
