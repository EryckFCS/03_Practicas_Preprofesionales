# Guía Operativa: Extracción de Datos en REDATAM para el Barrio El Capulí

Esta guía detalla el procedimiento para consultar la base de datos del **Censo de Población y Vivienda del Ecuador (INEC)** utilizando **RedatamX** (o el portal web REDATAM INEC).

---

## 1. Identificación Geográfica de la Zona en la Cartografía Censal

Para aislar el **Barrio El Capulí** en el cantón Loja:
* **Provincia:** `11` (Loja)
* **Cantón:** `1101` (Loja)
* **Parroquia:** `110156` (Punzara) o `110150` (Loja Urbana / cabecera)
* **Sectores Censales:** El Capulí comprende los sectores ubicados al margen suroriental del campus La Argelia (Av. Reinaldo Espinosa, sector Capulí Loma, inmediaciones del Colegio San Gerardo).

---

## 2. Apertura del Software y Selección del Diccionario

1. Abra **RedX Process** (o Redatam Desktop) desde el menú de inicio (`C:\Program Files\RedatamX\RedX Process.exe`).
2. Vaya a `Archivo` -> `Abrir Diccionario (.dicx / .dic)`.
3. Seleccione el diccionario del Censo de Población y Vivienda:
   * Ejemplo: `CPV2022_ECU.dicx` o la base descargada del portal INEC.

---

## 3. Consultas Frecuentes Requeridas por la Docente

### A. Población Total y Pirámide de Edades (Entidad: Persona)
* **Variables:**
  * `SEXO` (Hombre, Mujer)
  * `EDAD` (Grupos quinquenales: 0-4, 5-9, 10-14, ..., 65+)
* **Filtro de Área Geográfica:**
  ```text
  SELECCION = PROVINCIA = 11 AND CANTON = 1101 AND PARROQUIA = 56
  ```
* **Tipo de Tabulado:** Cruce de variables (`Crosstabs`: Edad vs. Sexo).
* **Salida:** Exportar a `.xlsx` o `.csv` para alimentar Stata.

### B. Condiciones de Vivienda y Materialidad (Entidad: Vivienda)
* **Variables:**
  * `TIPO_VIV` (Casa/Villa, Departamento, Mediagua, Choza, etc.)
  * `PAREDES` (Hormigón, Ladrillo/Bloque, Madera, Caña)
  * `TECHO` (Losa, Zinc, Teja, Paja)
  * `ESTADO_VIV` (Bueno, Regular, Malo)

### C. Servicios Básicos (Entidad: Vivienda)
* **Variables:**
  * `AGUA` (Red pública dentro de la vivienda, red pública fuera, pozo, carro cisterna)
  * `ALCANTARILLADO` (Red pública de alcantarillado, pozo séptico, pozo ciego)
  * `LUZ` (Red pública de electricidad)
  * `BASURA` (Carro recolector, arrojan a terreno/río, queman)

### D. Pobreza NBI y Hacinamiento (Entidad: Hogar / Persona)
* **Variables:**
  * `NBI` (Condición de pobreza por Necesidades Básicas Insatisfechas: Pobre / No Pobre)
  * `NUM_DORM` (Número de dormitorios) vs. `NUM_PER` (Número de personas en el hogar) -> Cálculo de hacinamiento (> 3 personas/dormitorio).

---

## 4. Exportación de Resultados para QGIS y Stata

1. Al generar el tabulado, haga clic en el botón **Exportar** (`Excel` o `Texto delimitado CSV`).
2. Guarde los archivos con nomenclatura estandarizada en:
   `docs/vaults/v01-diagnostico-territorial-el-capuli/datos_redatam/`
   * Ejemplo: `capuli_poblacion_edad_sexo.csv`
   * Ejemplo: `capuli_servicios_vivienda_manzana.csv`
3. Asegúrese de incluir siempre el **código identificador de manzana o sector (`cod_sector` / `cod_manzana`)** en los tabulados agregados para permitir el **Join espacial en QGIS**.
