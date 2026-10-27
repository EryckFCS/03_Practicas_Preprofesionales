# Exportación de Datos de KoboToolbox hacia QGIS, AutoCAD y Revit
## De la Base de Datos en la Nube al Plano Arquitectónico y Urbano

> **Destinatarios:** Docentes, tutores y estudiantes para procesar los datos levantados y transformarlos en insumos de diseño.

---

## 1. Descarga desde el Panel Web de KoboToolbox

1. Ingrese a la plataforma web de KoboToolbox con la cuenta administradora del proyecto.
2. Haga clic sobre el proyecto: `Ficha de Diagnóstico Arquitectónico y Predial - UNL 2026`.
3. Vaya a la pestaña superior **"Datos"** $\rightarrow$ submenú lateral **"Descargas"**.

### Formatos a Descargar:

| Formato | Uso Arquitectónico | Configuración Recomendada |
| :--- | :--- | :--- |
| **XLS (Excel)** | Cuadros de áreas, estadísticas, NBI | Tipo de exportación: *XLS*. Versión de etiquetas: *Etiquetas de opciones*. |
| **GeoJSON** | Carga directa en QGIS o ArcGIS | Tipo de exportación: *GeoJSON*. Incluye las coordenadas GPS automáticas. |
| **Medios (.ZIP)**| Banco de fotografías técnicas | Tipo de exportación: *Archivos adjuntos (fotos)*. Guarda las imágenes nombradas por predio. |

---

## 2. Incorporación y Geoprocesamiento en QGIS

1. Abra **QGIS** (versión 3.28 o superior).
2. Establezca el Sistema de Referencia de Coordenadas (SRC) del proyecto en:  
   👉 **WGS 84 / UTM Zona 17S (EPSG: 32717)** (Sistema oficial para Loja y la mayor parte del Ecuador).
3. Arrastre el archivo `.geojson` descargado de KoboToolbox directamente sobre el lienzo de QGIS.
4. Los puntos aparecerán georreferenciados sobre la cartografía base (OpenStreetMap o imagen satelital de Google Hybrid).
5. **Simbolización Temática por Variable:**
   - Clic derecho en la capa $\rightarrow$ **Propiedades** $\rightarrow$ **Simbología**.
   - Cambie de *Símbolo Único* a **Categorizado**.
   - Seleccione el campo a mapear: por ejemplo, `estado_conservacion` o `estructura_principal`.
   - Asigne colores normativos (Verde: Bueno, Amarillo: Regular, Rojo: Malo o Crítico).

---

## 3. Exportación a AutoCAD (.DXF / .DWG)

Para llevar los puntos y datos hacia el software de dibujo técnico CAD:

### Método Directo desde QGIS:
1. Con la capa de puntos cargada y filtrada en QGIS:
2. Clic derecho en la capa de KoboToolbox $\rightarrow$ **Exportar** $\rightarrow$ **Guardar objetos como...**
3. En **Formato**, elija: **Archivo DXF de AutoCAD [AutoCAD DXF]**.
4. En **SRC**, seleccione **EPSG: 32717** (fundamental para que las distancias estén en metros reales y no en grados geográficos).
5. En la sección **Codificación y Atributos**, active la casilla para exportar etiquetas de texto con el número de lote y número de pisos.
6. Guarde el archivo como `levantamiento_campo_capuli.dxf`.
7. Al abrir el archivo en **AutoCAD**:
   - Ejecute el comando `ZOOM` $\rightarrow$ opción `EXTENSIÓN` (`Z` + `E`).
   - Los puntos y textos aparecerán en sus coordenadas exactas en metros, listos para dibujar poligonales de linderos, retiros y perfiles viales.

---

## 4. Auditoría de Calidad Post-Descarga (Control Docente)

Antes de validar los estudios técnicos para edificación, el equipo revisor debe verificar en la tabla de atributos de Excel/QGIS:

```text
[CHECKLIST DE APROBACIÓN]
[ ] 1. 0% de campos nulos en variables estructurales de predios habitados.
[ ] 2. 100% de los puntos GPS se ubican dentro del perímetro de estudio.
[ ] 3. Ningún punto tiene precisión registrada > 5.0 metros.
[ ] 4. Cada registro cuenta con su fotografía de fachada verificable.
[ ] 5. Los datos de frente y fondo guardan relación con el catastro oficial.
```
