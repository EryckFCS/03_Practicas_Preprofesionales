# Informe Técnico de Cruce Metodológico: Ficha A.R.R. vs Encuesta KoboToolbox

Diagnóstico Territorial y Comunitario — Barrio El Capulí (Punzara, Loja)

---

## 1. Naturaleza Metodológica de Ambos Instrumentos

| Dimensión | Ficha A.R.R. (`CAMPOS ARR.xls`) | Encuesta KoboToolbox (`encuesta capuli arquitectura`) |
| :--- | :--- | :--- |
| **Nivel de Observación** | **Mesotorritorial / Comunitario (Líderes, Ficha Barrial)** | **Microterritorial / Hogar (Familias e Individuos)** |
| **Informante Clave** | Presidente del Barrio, Directiva, Personal de Salud/Escuela | Jefe de Hogar / Morador encuestado |
| **Propósito** | Inventario físico de equipamientos, vías, escuelas y servicios | Condiciones de habitabilidad, necesidades básicas y percepción |
| **Total de Variables** | 386 campos temáticos (22 capítulos) | 115 variables estructuradas |

---

## 2. Preguntas que se Cruzan Directamente (Coincidencias Clave)

Estas preguntas miden la misma variable y deben mantenerse consistentes entre la ficha del líder barrial y la encuesta de hogar:

| Variable Territorial | Pregunta en Encuesta Kobo (Hogar) | Campo Homólogo en Ficha A.R.R. (Comunidad) |
| :--- | :--- | :--- |
| `integer` | ¿Cuántos años cumplidos tiene? | 17.1 Ha sufrido daños la comunidad por causa de: |
| `select_one` | ¿Cómo se identifica según su cultura y costumbres? | 2.1 Grupo étnico predominante en la comunidad |
| `select_multiple` | ¿Cuál es su ocupación? | 22.2 Tipo de actividad en la que participan |
| `select_one` | ¿Cómo calificaría  la vía de acceso a su hogar? | 7.11 Distancia a la que abordan cualquier tipo de transporte motorizados (kms) |
| `select_one` | ¿Normalmente tiene acceso a electricidad en su hogar? | 8.3 Qué porcentaje de la población tiene energía eléctrica |
| `select_one` | ¿Normalmente tiene acceso a agua potable en su hogar? | 9.3 Fuente principal de abasto / Qué tipo de agua se consume |
| `select_one` | ¿Cómo calificaría el acceso de agua en su hogar? | 9.1a Existe red de agua entubada: |
| `select_one` | ¿Cuenta con servicio de recolección de basura en su área? | 9.6 Cómo disponen o eliminan la basura en la comunidad |
| `select_one` | ¿Cómo calificaría el servicio de recolección de basura en su área? | 9.6 Cómo disponen o eliminan la basura en la comunidad |
| `select_one` | ¿Su vivienda esta conectada al sistema de alcantarillado público? | 9.4a Existe sistema de alcantarillado en la comunidad |
| `select_one` | ¿Qué sistema utiliza para la descarga de agua residuales? | 9.1a Existe red de agua entubada: |
| `range` | ¿Qué tan satisfecho está con su trabajo actual? | 16.2d Qué actividades incompatibles existen? |
| `range` | ¿Qué tan satisfecho está con la calidad del medio ambiente? | 16.1 Protegen el medio Ambiente |
| `range` | ¿Qué tan satisfecho está con el desempeño del gobierno? | 20.10 Qué servicios recibe la comunidad del municipio - Otros |
| `select_one` | ¿Qué tan satisfecho está con la comunidad en la que vive? | 21.3 Existe en la comunidad una comisaría de la mujer: |
| `range` | ¿Que tan satisfecho se siente con el gobierno municipal de Loja? | 20.1 Qué servicios recibe la comunidad del municipio - Feria de animales |
| `score__row` | ¿Considera Usted que, la mayoría de personas en este barrio o comunidad se llevan bien entre ellos? | 15.1.6 Cuantas actividades productivas existen en la comunidad - talleres(mecánicos, eléctricos) |
| `score__row` | ¿En general, Usted considera que puede confiar en la mayoría de las personas de este barrio o comunidad? | 22.4a Necesidades mayores de la comunidad |
| `score__row` | ¿Siente Usted que es parte de este barrio o comunidad? | 7.9 Existe servicio de transporte a la comunidad |
| `range` | ¿Qué tan confiado se siente con la Administración de Justicia? | 21.4 Existe puesto de policía o retén en la comunidad: |
| `range` | ¿Qué tan confiado se siente con la Policía Nacional? | 21.4 Existe puesto de policía o retén en la comunidad: |
| `select_one` | ¿Ha sido víctima de robo de auto en el último año? | 21.4 Existe puesto de policía o retén en la comunidad: |
| `select_one` | ¿Ha sido víctima de robo en su hogar en el último año? | 21.4 Existe puesto de policía o retén en la comunidad: |
| `select_one` | ¿Ha sido víctima de algún crimen en el último año? | 21.4 Existe puesto de policía o retén en la comunidad: |
| `score__row` | ¿Recicla residuos orgánicos? | 16.1 Protegen el medio Ambiente |

---

## 3. Estructura de Capítulos de la Ficha A.R.R. (386 campos)

### 1. Demografía y Población (Cap 1-3) (40 campos)
- 1.5 Zona
- 1.6 Sector
- 1.7 Area
- 2.1 Grupo étnico predominante en la comunidad
- 3.1 Número de habitantes de la comunidad
- 3.2a Niños menores de 1 año
- *... y 34 campos adicionales.*

### 2. Accesibilidad, Vías y Transporte (Cap 4, 7) (86 campos)
- 4.1a Distancia a la cabecera parroquial (Km)
- 4.1b Tiempo (horas) a la cabecera parroquial transporte 1
- 4.1c Tiempo (horas) a la cabecera parroquial transporte 2
- 4.1d Tiempo (horas) a la cabecera parroquial transporte 3
- 4.1e Tiempo (horas) a la cabecera parroquial transporte 4
- 4.1f Transporte 1
- *... y 80 campos adicionales.*

### 3. Educación y Desarrollo Infantil (Cap 5) (27 campos)
- 5.1 Existen instituciones educativas y de Desarrollo Infantil (públicas ó privadas) en la comunidad:
- 5.3 Las escuelas de la comunidad pertenecen a las redes educativas o CEM?
- 5.4a A cuál institución asisten los niños / jovenes de la comunidad - Escuela nombre
- 5.5 Parroquia o cabecera cantonal a la cual pertenece la escuela
- 5.5 Se encuentra en una Cabecera Cantonal, Parroquia o Comunidad
- 5.6 Distancia de la institución a la que asisten (kms):
- *... y 21 campos adicionales.*

### 4. Salud y Establecimientos (Cap 6) (28 campos)
- 6.1 Existen establecimientos de salud en la comunidad
- 6.2.1 Instancias y/o establecimientos de salud que existen - Parteras capacitadas
- 6.2.2 Instancias y/o establecimientos de salud que existen - Parteras no capacitadas
- 6.2.3 Instancias y/o establecimientos de salud que existen - Promotores de salud
- 6.2.4 Instancias y/o establecimientos de salud que existen - Curandero tradicional
- 6.2.5 Instancias y/o establecimientos de salud que existen - Shaman
- *... y 22 campos adicionales.*

### 5. Servicios Básicos e Infraestructura (Cap 8, 9) (35 campos)
- 8.1 Existe servicio de energía eléctrica en la comunidad:
- 8.2 Qué tipo de servicio:
- 8.3 Qué porcentaje de la población tiene energía eléctrica
- 8.4 Distancia al lugar más cercano con energía eléctrica (kms):
- 8.4a Minutos al lugar más cercano con energía eléctrica :
- 8.4b Energía Eléctrica Alternativa
- *... y 29 campos adicionales.*

### 6. Economía, Producción y Suelo (Cap 10-15) (65 campos)
- 10.1a Actividades económicas principales se dedica la población
- 10.2b Actividades económicas principales se dedica la población
- 10.1c Actividades económicas principales se dedica la población
- 10.1d Actividades económicas principales se dedica la población
- 10.1e Actividades económicas principales se dedica la población
- 10.2a Cuales son las tres actividades productivas más rentables de la comunidad
- *... y 59 campos adicionales.*

### 7. Medio Ambiente y Riesgos (Cap 16, 17) (11 campos)
- 16.1 Protegen el medio Ambiente
- 16.2a Existen áreas naturales protegidas
- 16.2b Qué áreas naturales protegidas son?
- 16.2c Se realizan actividades incompatibles
- 16.2d Qué actividades incompatibles existen?
- 16.3 Existe desechos industriales
- *... y 5 campos adicionales.*

### 8. Turismo y Equipamientos Especiales (Cap 18) (25 campos)
- 18.1.1 Servicios turísticos - Hoteles / alojamiento / hospedaje
- 18.1.2 Servicios turísticos - Restaurant / Alimentación
- 18.1.3 Servicos turísticos - Bares
- 18.1.4 Servicios turísticos - Transporte para turistas
- 18.1.5 Servicios turísticos - Servicio de guias
- 18.1.6 Servicios turísticos - Cybercafes
- *... y 19 campos adicionales.*

### 9. Apoyo Institucional, Municipio y Comunidad (Cap 19-22) (69 campos)
- CAMPOS A LEVANTAR POR  A.R.R.  PARA LA CARACTERIZACIÓN DE LAS COMUNIDADES
- 5,11a Hombres Analfabetos Cuantos
- 5,11b Mujeres Analfabetas Cuantas
- 5,11c Hombres y Mujeres Analfabetos Cuantos
- 19.1 Reciben la comunidad o parte de ella, asistencia técnica / financiera:
- 19.1a De qué instituciones reciben ayuda - nacional - nombre
- *... y 63 campos adicionales.*

