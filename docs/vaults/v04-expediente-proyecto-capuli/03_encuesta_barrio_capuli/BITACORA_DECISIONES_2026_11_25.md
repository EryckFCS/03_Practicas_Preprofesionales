# Bitácora de Decisiones y Cambios · 2026-11-25

- **Fecha:** `2026-11-25`
- **Rama activa:** `feat/expediente-capuli-giz`
- **Ámbito:** Expediente Barrio El Capulí, Zona de Influencia Indirecta `ZII-01` y Área Periurbana de los `9` Asentamientos Sur

---

## 1. Decisión metodológica · Encaje de barrios por sector censal INEC

Ante la falta de coincidencia geométrica entre límites barriales o comunitarios y los sectores censales `sec_a` del INEC, se adoptó oficialmente la metodología de **partición `Barrio ∩ Sector Censal` con desagregación dasimétrica ponderada por edificaciones `edif_p`**:

1. **Partición cartográfica sin deformación:** cada una de las `27` unidades operativas —`9` sectores de El Capulí, `ZII-01` y `17` sectores periurbanos— se intersecó con la capa oficial `sec_a` de `11_loja.gpkg`, generando **`46` subpolígonos limpios** en la capa `00j_barrios_por_sector_censal_inec`. Ningún subpolígono cruza dos sectores censales distintos.
2. **Ponderación dasimétrica por viviendas `edif_p`:** para evitar el sesgo de sumar sectores censales enteros o ponderar por hectáreas deshabitadas, cada subpolígono recibe el peso `w = n_viv_interseccion / n_viv_sector_inec` calculado sobre edificaciones residenciales reales del CPV 2022.

### Resultados verificados por sector censal INEC

| Sector INEC | Unidades intersectadas | Área cubierta ha | Viviendas en unidades | Viviendas totales sector INEC | Suma pesos `w` | Cobertura del sector % |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `110150059008` | 2 | 21.51 | 14 | 104 | 0.1346 | 13.46 |
| `110150063006` | 4 | 28.19 | 38 | 96 | 0.3958 | 39.58 |
| `110150063007` | 5 | 29.51 | 114 | 128 | 0.8906 | 89.06 |
| `110150063008` | 6 | 26.31 | 134 | 136 | 0.9854 | 98.54 |
| `110150999023` | 3 | 156.48 | 43 | 128 | 0.3359 | 33.59 |
| `110150999024` | 2 | 104.72 | 89 | 91 | 0.9780 | 97.80 |
| `110150999025` | 7 | 113.95 | 46 | 46 | 1.0000 | 100.00 |
| `110150999026` | 5 | 160.31 | 76 | 116 | 0.6552 | 65.52 |
| `110150999028` | 4 | 195.43 | 89 | 93 | 0.9570 | 95.70 |
| `110150999029` | 8 | 177.39 | 80 | 85 | 0.9412 | 94.12 |

En total se asignaron **`723` viviendas residenciales `edif_p`** en `46` subpolígonos distribuidos en `10` sectores censales poblados de `11` sectores INEC intersectados.

---

## 2. Trazabilidad auditada de manzanas censales `man_a`

- **Archivo crudo original:** `lake/raw/11_LOJA.zip` de `101.60 MB`, que contiene el GeoPackage provincial `11_loja.gpkg` de `205.30 MB` con `9` capas oficiales INEC en `EPSG:31992`.
- **Copia descomprimida de trabajo:** `docs/vaults/v01-diagnostico-territorial-el-capuli/cartografia_qgis/11_loja.gpkg`.
- **Carpeta temporal de capacitación en QGIS:** se generó `practica_extraccion_manzanas_temp/` con los Shapefiles de insumo y resultado esperado más `GUIA_PASO_A_PASO_QGIS.md` para replicar manualmente la extracción de `man_a`.

---

## 3. Archivos creados y editados el 2026-11-25

- `scripts/generar_matriz_barrio_sector_censal.py`: script reproducible de intersección `Barrio ∩ Sector Censal` y pesos dasimétricos por `edif_p`.
- `qgis/01_proyecto_principal/proyecto_principal_capuli_y_periurbano.gpkg`: incorporada la capa espacial `00j_barrios_por_sector_censal_inec`.
- `qgis/01_proyecto_principal/proyecto_principal_capuli_y_periurbano.qgz`: incorporada la capa `Encaje Barrio x Sector Censal INEC · 46 subpolígonos`.
- `qgis/01_proyecto_principal/matriz_barrio_sector_censal_pesos_edif.csv` y `.xlsx`: matrices de correspondencia y resumen por sector censal INEC.
- `assets/mapa_encaje_barrios_sectores_censales.png`: lámina cartográfica diagnóstica del encaje por sector censal.
- `BITACORA_DECISIONES_2026_11_25.md`: registro de la decisión metodológica y cambios del día para el commit en `feat/expediente-capuli-giz`.
