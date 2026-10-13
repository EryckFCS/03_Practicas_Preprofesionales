# Matriz de Indicadores Territoriales y Poblacionales — Barrio El Capulí

Matriz estructurada de variables e indicadores cuantitativos para el diagnóstico base del proyecto de vinculación en Arquitectura.

---

## 1. Bloque Sociodemográfico

| Código | Indicador | Fuente | Nivel Geográfico | Fórmula / Definición |
| :--- | :--- | :--- | :--- | :--- |
| **DEM-01** | Población Total | CPV INEC (Redatam) | Manzana / Sector | $\sum P_i$ (Total de residentes habituales) |
| **DEM-02** | Relación Hombre / Mujer | CPV INEC (Redatam) | Sector | $(P_{hombres} / P_{mujeres}) \times 100$ |
| **DEM-03** | Población en Edad Escolar (0-14 años) | CPV INEC (Redatam) | Sector | Población de 0 a 14 años cumplidos |
| **DEM-04** | Adultos Mayores (65+ años) | CPV INEC (Redatam) | Sector | Población de 65 años o más |
| **DEM-05** | Índice de Dependencia Demográfica | CPV INEC (Redatam) | Sector | $[(P_{0-14} + P_{65+}) / P_{15-64}] \times 100$ |
| **DEM-06** | Densidad Bruta Poblacional | Redatam + QGIS | Manzana | $\text{Habitantes} / \text{Área de Manzana (ha)}$ |

---

## 2. Bloque Habitacional y Condiciones de Vivienda

| Código | Indicador | Fuente | Nivel Geográfico | Relevancia para Arquitectura |
| :--- | :--- | :--- | :--- | :--- |
| **VIV-01** | Total de Viviendas Particulares | CPV INEC (Redatam) | Manzana | Cuantificación del parque habitacional. |
| **VIV-02** | Viviendas Ocupadas con Personas Presentes | CPV INEC (Redatam) | Manzana | Ocupación real vs. viviendas deshabitadas/lotes. |
| **VIV-03** | Materialidad Predominante (Paredes) | CPV INEC (Redatam) | Sector | Tipología constructiva (Ladrillo/hormigón vs. precario). |
| **VIV-04** | Materialidad Predominante (Cubierta/Techo) | CPV INEC (Redatam) | Sector | Análisis de vulnerabilidad estructural y durabilidad. |
| **VIV-05** | Déficit Cualitativo de Vivienda | CPV INEC / Metodología MIDUVI | Sector | Viviendas con materiales deficientes o sin servicios. |
| **VIV-06** | Tasa de Hacinamiento Crítico | CPV INEC (Redatam) | Sector | Hogares con más de 3 personas por dormitorio. |

---

## 3. Bloque de Cobertura de Infraestructura y Servicios Básicos

| Código | Indicador | Fuente | Nivel Geográfico | Estándar de Cobertura |
| :--- | :--- | :--- | :--- | :--- |
| **SER-01** | Cobertura de Agua Potable por Red | CPV INEC (Redatam) | Manzana / Sector | % de viviendas conectadas a la red pública. |
| **SER-02** | Cobertura de Alcantarillado Sanitario | CPV INEC (Redatam) | Manzana / Sector | % de viviendas con red de alcantarillado. |
| **SER-03** | Servicio de Recolección de Basura | CPV INEC (Redatam) | Sector | % de viviendas atendidas por el carro recolector. |
| **SER-04** | Acceso a Energía Eléctrica | CPV INEC (Redatam) | Manzana / Sector | % de viviendas con suministro eléctrico formal. |

---

## 4. Bloque Socioeconómico y Pobreza

| Código | Indicador | Fuente | Nivel Geográfico | Uso para Planificación |
| :--- | :--- | :--- | :--- | :--- |
| **SOC-01** | Pobreza por NBI General | CPV INEC (Redatam) | Sector | Hogares con al menos una necesidad básica insatisfecha. |
| **SOC-02** | NBI por Capacidad de Subsistencia | CPV INEC (Redatam) | Sector | Escolaridad del jefe del hogar y tasa de dependencia económica. |
| **SOC-03** | Acceso a Internet y Conectividad | CPV INEC (Redatam) | Sector | Brecha digital en el territorio. |

---

## 5. Bloque de Equipamiento y Espacio Público (Validación de Campo con Arquitectura)

| Código | Indicador | Técnica de Levantamiento | Responsable |
| :--- | :--- | :--- | :--- |
| **EQU-01** | Distancia a Paradas de Transporte Urbano | QGIS (Análisis de Red / Buffers) | Economía & Arquitectura |
| **EQU-02** | Radio de Cobertura de Espacios Verdes / Canchas | QGIS (Buffers de 300m / 500m) | Arquitectura |
| **EQU-03** | Estado Físico de Vías y Aceras | Ficha de Inspección Visual | Trabajo conjunto en territorio |
| **EQU-04** | Disponibilidad de Lotes Baldíos / Suelo Vacante | Catastro / QGIS | Arquitectura |
