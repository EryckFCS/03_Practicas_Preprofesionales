# Protocolo Cartográfico en QGIS — Diagnóstico Barrio El Capulí

Este protocolo describe los pasos para generar la cartografía temática y los mapas de calor requeridos por la docente y el equipo de Arquitectura.

---

## 1. Sistema de Referencia Espacial (SRC Obligatorio)

* Para la ciudad y provincia de Loja, configure siempre el proyecto en:
  * **EPSG: 32717** — `WGS 84 / UTM zone 17S`.
  * *Verificar en la esquina inferior derecha de QGIS que figure `EPSG:32717`.*

---

## 2. Insumos Cartográficos Necesarios

1. **Cartografía Censal INEC (Shapefile / GeoPackage):**
   * Cobertura de Manzanas Censales (`manzanas_censales_loja.shp`) o Sectores Censales.
   * Descargable del Geoportal del INEC (Geocatálogo CPV).
2. **Capa Base de Vialidad y Contexto:**
   * OpenStreetMap (QuickMapServices plugin o XYZ Tiles: `https://tile.openstreetmap.org/{z}/{x}/{y}.png`).
   * Curvas de nivel y relieve de Loja (IGM 1:50.000).
3. **Tabulados de Datos REDATAM:**
   * Archivo CSV en `datos_redatam/capuli_indicadores_manzanas.csv`.

---

## 3. Procedimiento de Unión de Atributos (Table Join)

1. En QGIS, agregue la capa vectorial de manzanas censales:
   * `Capa` -> `Añadir Capa` -> `Añadir capa vectorial...`
2. Agregue la tabla de datos de Redatam:
   * `Capa` -> `Añadir Capa` -> `Añadir capa de texto delimitado...` (o arrastre el archivo `.csv`).
3. Clic derecho en la capa de manzanas censales -> `Propiedades` -> Pestaña **Uniones (Joins)**:
   * Haga clic en el botón verde `+` (Añadir nueva unión).
   * **Capa de unión:** Seleccione la tabla CSV de Redatam.
   * **Campo de unión:** `cod_manzana` (del CSV).
   * **Campo objetivo:** `COD_MANZ` o `ID_MANZ` (del shapefile).
   * Marque las columnas deseadas: Población, NBI, Servicios, etc.
   * Haga clic en `Aceptar`.

---

## 4. Generación de Mapas Temáticos Solicitados

### A. Mapa de Calor (Heatmap) de Distribución Poblacional
1. Clic derecho en la capa unida -> `Propiedades` -> `Simbología`.
2. En el tipo de renderizador superior, seleccione **`Mapa de calor (Heatmap)`**.
3. **Ponderar por (Weight by):** Seleccione el campo de población unida (`POB_TOTAL`).
4. **Radio:** Configure entre `30` y `50` metros (dependiendo de la densidad de manzanas).
5. **Rampa de color:** Seleccione `Magma`, `Viridis` o `Reds`.
6. En `Representación de capa`, reduzca la opacidad al 75% para visualizar las calles de fondo.

### B. Mapa de Vulnerabilidad y NBI (Coropletas)
1. Tipo de renderizador: **`Graduado`**.
2. **Valor:** Seleccione `%_NBI` o `Tasa_Hacinamiento`.
3. **Modo:** `Intervalos naturales (Jenks)` con 4 o 5 clases.
4. **Rampa de color:** `YlOrRd` (Amarillo a Rojo para indicar mayor vulnerabilidad).

---

## 5. Salidas para el Equipo de Arquitectura

1. **Diseño de Impresión (Compositor de Mapas):**
   * Cree una lámina formato A3 o A4 (`Proyecto` -> `Nueva composición de impresión`).
   * Añada mapa, barra de escala gráfica, norte geográfico, leyenda clara y membrete institucional UNL (Economía / Arquitectura).
   * Exporte a PDF y PNG (300 DPI) hacia:
     `docs/vaults/v01-diagnostico-territorial-el-capuli/evidencias/`
2. **Intercambio con CAD (AutoCAD / Revit):**
   * Exporte las capas vectoriales filtradas a DXF:
     `Capa` -> `Exportar` -> `Guardar objetos como...` -> Formato `AutoCAD DXF` para que los estudiantes de arquitectura puedan integrarlo a sus planos base.
