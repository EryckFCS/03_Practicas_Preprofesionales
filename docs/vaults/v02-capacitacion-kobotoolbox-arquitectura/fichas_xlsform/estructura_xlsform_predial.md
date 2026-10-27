# Estructura de Ficha Técnica XLSForm para Arquitectura y Urbanismo
## Plantilla Estándar: Diagnóstico Físico-Espacial y Habitacional de Predios

La siguiente tabla describe la estructura técnica del archivo XLSForm (`survey`, `choices` y `settings`), diseñado específicamente para estudios previos de edificación y diagnósticos barriales (como El Capulí o áreas de intervención arquitectónica).

---

## 1. Hoja `survey` (Preguntas y Lógica)

| type | name | label::Español (es) | hint::Español (es) | required | constraint | constraint_message | relevant |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `start` | `hora_inicio` | | | | | | |
| `end` | `hora_fin` | | | | | | |
| `deviceid` | `id_dispositivo` | | | | | | |
| `begin_group` | `grp_identificacion` | Identificación del Predio y del Levantamiento | | | | | |
| `text` | `cod_estudiante` | Código o Nombre del Estudiante Responsable | Ejemplo: COND_01 | yes | `regex(., '^[A-Z]{3,4}_[0-9]{2}$')` | Ingrese el código con formato AAA_00 (ej. COND_01) | |
| `text` | `cod_manzana` | Código de Manzana o Sector | Según plano base municipal | yes | `string-length(.) >= 3` | El código debe tener al menos 3 caracteres | |
| `integer` | `num_lote` | Número de Lote / Predio | Número asignado en planimetría | yes | `. >= 1 and . <= 999` | El número de lote debe estar entre 1 y 999 | |
| `geopoint` | `ubicacion_acceso` | Coordenada GPS del Acceso Principal | Espere a que la precisión sea $\le$ 5 metros | yes | | | |
| `end_group` | | | | | | | |
| `begin_group` | `grp_predio` | Dimensiones y Características del Suelo | | | | | |
| `decimal` | `frente_lote` | Frente del Lote hacia la Vía (metros) | Medida frontal con cinta o distanciómetro | yes | `. >= 4.0 and . <= 120.0` | Valor fuera de rango reglamentario (4 a 120 m) | |
| `decimal` | `fondo_lote` | Fondo Promedio del Lote (metros) | | yes | `. >= 6.0 and . <= 250.0` | Valor fuera de rango (6 a 250 m) | |
| `calculate` | `area_calculada` | | | | | | `${frente_lote} * ${fondo_lote}` |
| `select_one` `tipo_topografia` | `topografia` | Topografía Predominante del Terreno | | yes | | | |
| `select_one` `tipo_ocupacion` | `estado_ocupacion` | Estado Actual de Ocupación | | yes | | | |
| `end_group` | | | | | | | |
| `begin_group` | `grp_edificacion` | Datos Constructivos y Estructurales | | | | | `${estado_ocupacion} != 'baldio'` |
| `integer` | `num_pisos` | Número de Pisos Construidos | Contar niveles sobre el nivel de acera | yes | `. >= 1 and . <= 8` | El número de pisos debe ser entre 1 y 8 | |
| `select_one` `tipo_estructura` | `estructura_principal` | Sistema Estructural Predominante | Según Norma Ecuatoriana de la Construcción | yes | | | |
| `select_one` `tipo_muros` | `muros_predominantes` | Material de Mampostería / Paredes | | yes | | | |
| `select_one` `tipo_cubierta` | `cubierta_techo` | Material de Cubierta | | yes | | | |
| `select_one` `estado_edif` | `estado_conservacion` | Estado de Conservación General | | yes | | | |
| `select_one` `resp_sino` | `presenta_dano` | ¿Presenta Daños o Patologías Visibles? | Grietas, humedad severa, asentamientos | yes | | | |
| `select_multiple` `tipo_dano` | `patologias` | Tipología de Daño Detectado | Seleccione todas las que apliquen | yes | | | `${presenta_dano} = 'si'` |
| `image` | `foto_dano` | Fotografía de Detalle de la Patología | Tome la foto a 1.5 m con elemento de escala | yes | | | `${presenta_dano} = 'si'` |
| `end_group` | | | | | | | |
| `begin_group` | `grp_servicios` | Infraestructura y Servicios Básicos | | | | | |
| `select_multiple` `tipo_servicio` | `servicios_red` | Redes de Servicios con Acometida Activa | Verifique medidor o acometida real | yes | | | |
| `select_one` `tipo_via` | `acceso_vial` | Tipo de Superficie de la Vía Frontal | | yes | | | |
| `end_group` | | | | | | | |
| `begin_group` | `grp_evidencia` | Evidencia Fotográfica y Cierre | | | | | |
| `image` | `foto_fachada` | Fotografía de Fachada Principal Completa | Encuadre amplio que muestre predio y vía | yes | | | |
| `image` | `foto_entorno` | Fotografía del Entorno Inmediato | Relación con predios laterales | yes | | | |
| `text` | `observaciones` | Observaciones Técnicas Complementarias | Detalles relevantes para el proyecto | no | | | |
| `acknowledge` | `declaracion_veracidad`| Declaro bajo juramento que los datos levantados corresponden a la realidad física in situ | Marque para autorizar el envío del formulario | yes | | | |
| `end_group` | | | | | | | |

---

## 2. Hoja `choices` (Opciones Cerradas Estandarizadas)

| list_name | name | label::Español (es) |
| :--- | :--- | :--- |
| `resp_sino` | `si` | Sí |
| `resp_sino` | `no` | No |
| `tipo_topografia` | `plana` | Plano (Pendiente 0% a 5%) |
| `tipo_topografia` | `moderada` | Pendiente Moderada (6% a 15%) |
| `tipo_topografia` | `fuerte` | Pendiente Fuerte (16% a 30%) |
| `tipo_topografia` | `escarpada` | Escarpado / Quebrada (> 30%) |
| `tipo_ocupacion` | `consolidado` | Edificado y Habitado |
| `tipo_ocupacion` | `en_construccion` | En Proceso de Construcción |
| `tipo_ocupacion` | `deshabitado` | Edificado pero Desocupado / Abandonado |
| `tipo_ocupacion` | `baldio` | Terreno Baldío / Sin Construcción |
| `tipo_estructura` | `ha_porticos` | Hormigón Armado (Pórticos: vigas y columnas) |
| `tipo_estructura` | `metalica` | Estructura Metálica (Perfiles de acero) |
| `tipo_estructura` | `madera` | Estructura de Madera |
| `tipo_estructura` | `mixta` | Mixta (Hormigón + Metal o Madera) |
| `tipo_estructura` | `autoportante` | Mampostería Portante (Ladrillo confinado) |
| `tipo_estructura` | `tradicional` | Tierra cruda (Adobe / Tapial / Bahareque) |
| `tipo_muros` | `ladrillo` | Ladrillo panel / cocido |
| `tipo_muros` | `bloque` | Bloque de cemento / hormigón |
| `tipo_muros` | `adobe` | Adobe o tapial |
| `tipo_muros` | `madera_tabla` | Tabla o listón de madera |
| `tipo_muros` | `prefabricado` | Panel prefabricado / fibrocemento |
| `tipo_cubierta` | `losa_ha` | Losa de hormigón armado |
| `tipo_cubierta` | `zinc_techo` | Lámina de zinc / acerolit |
| `tipo_cubierta` | `teja_ceramica` | Teja de arcilla cocida |
| `tipo_cubierta` | `fibrocemento` | Planchas de fibrocemento |
| `estado_edif` | `bueno` | Bueno (No requiere reparaciones estructurales) |
| `estado_edif` | `regular` | Regular (Deterioro en acabados o fisuras menores) |
| `estado_edif` | `malo` | Malo (Fisuras activas, deformaciones, desprendimiento) |
| `estado_edif` | `ruinoso` | Ruinoso (Riesgo inminente de colapso) |
| `tipo_dano` | `asentamiento` | Asentamiento diferencial de cimientos |
| `tipo_dano` | `fisura_estructural` | Fisuras o grietas en columnas/vigas |
| `tipo_dano` | `grieta_muros` | Grietas diagonales en paredes |
| `tipo_dano` | `humedad_severa` | Humedad ascendente o filtración severa |
| `tipo_dano` | `deflexion_losa` | Pandeo o flecha visible en losas/cubiertas |
| `tipo_servicio` | `agua_red` | Red Pública de Agua Potable |
| `tipo_servicio` | `alcantarillado` | Red de Alcantarillado Sanitario |
| `tipo_servicio` | `electricidad` | Red de Energía Eléctrica |
| `tipo_servicio` | `alumbrado_publico` | Alumbrado Público en Vía |
| `tipo_servicio` | `telefonia_internet` | Telefonía Fija / Fibra Óptica |
| `tipo_via` | `asfalto` | Asfalto / Pavimento Flexible |
| `tipo_via` | `hormigon` | Pavimento Rígido (Hormigón) |
| `tipo_via` | `adoquin` | Adoquín |
| `tipo_via` | `lastrado` | Lastrado / Cascajo afirmado |
| `tipo_via` | `tierra` | Tierra / Camino de herradura |

---

## 3. Hoja `settings`

| form_title | form_id | version | default_language |
| :--- | :--- | :--- | :--- |
| Ficha de Diagnóstico Arquitectónico y Predial | ficha_arq_unl_2026 | 2026101901 | Español (es) |
