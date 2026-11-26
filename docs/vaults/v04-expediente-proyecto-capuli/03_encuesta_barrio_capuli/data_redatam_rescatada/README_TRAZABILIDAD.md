# Trazabilidad de insumos REDATAM CPV 2022 rescatados

Este directorio almacena únicamente los insumos verificados y rescatados desde `C:\Users\ERICK-FCS\Downloads\repaso.zip` el `2026-11-25`, sin sobrescribir ni alterar la cartografía maestra ni el proyecto QGIS en `qgis/01_proyecto_principal/`.

## Archivos rescatados

1. **Base REDATAM CPV 2022 por manzana y localidad** en `lake/raw/redatam_cpv2022_manloc/`:
   - `CPV_2022_REDATAM_MANLOC.zip` de `409.58 MB`, copia única sin duplicados.
   - `CPV2022_ReporteGeneracion.xlsx`.
2. **Sectorización barrial municipal** en `lake/raw/capas_municipio/sectorizacion_barrial/`:
   - `Sectorizacion_barrial.shp` y archivos auxiliares, `213` sectores barriales de Loja con atributos `PRESIDENTE` y `CONTACTO`.
3. **Tablas Excel de El Capulí exportadas desde REDATAM CPV 2022** en esta carpeta:
   - `Codigos_Manzanas_Capuli.xlsx`
   - `Poblacion_Manzanas_Capuli_2022.xlsx`
   - `VARIABLES_CAPULI.xlsx`
   - `Variables_Persona_Capuli_2022.xlsx`
   - `VARIABLES_HOGAR_CAPULI_2022.xlsx`
   - `variables_Vivienda_Capuli_2022.xlsx`
   - `VARIABLE_MORTALIDAD_CAPULI_2022.xlsx`
   - `VARIABLE_EMIGRANTES_CAPULI_2022.xlsx`

## Archivos de selección REDATAM corregidos

Para evitar los errores detectados en los JSON originales de `repaso.zip`, se generaron dos archivos de selección corregidos listos para importar en REDATAM:

- `Sectores_Periurbanos_Corredor_Sur_2022_CORREGIDO_sel.json`: incluye los `6` sectores censales periurbanos reales del corredor sur `110150999023`, `110150999024`, `110150999025`, `110150999026`, `110150999028` y `110150999029`. Corrige la omisión de `999025` y `999029` y excluye los sectores ajenos `999007` y `999027`.
- `Seleccion_Manzanas_Capuli_29_CORREGIDO_sel.json`: incluye las `29` manzanas exactas de `00d_manzanas_inec_capuli`.

## Advertencia metodológica

Las tablas Excel de El Capulí rescatadas desde `repaso.zip` fueron exportadas sobre `21` manzanas censales completas sin recorte al límite oficial del barrio de `115.12 ha`, por lo que sus totales de `1,361` personas, `353` hogares y `405` viviendas sobreestiman la población estrictamente residente dentro del polígono oficial de Barrio El Capulí. Para el análisis espacial estricto del barrio y los sectores periurbanos prevalecen las estimaciones dasimétricas basadas en `edif_p` de `qgis/01_proyecto_principal/`.
