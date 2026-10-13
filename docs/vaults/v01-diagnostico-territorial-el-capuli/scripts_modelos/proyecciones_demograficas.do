* ==============================================================================
* PROYECCIONES DEMOGRÁFICAS — BARRIO EL CAPULÍ (LOJA)
* Prácticas Preprofesionales: Economía & Arquitectura (UNL)
* Autor: Eryck Condoy
* ==============================================================================

clear all
set more off

* Definición de rutas relativas
local data_dir "../datos_redatam"
local out_dir  "../evidencias"

* 1. Parámetros de Población Base (Datos censales INEC)
* P_2010: Población Censo 2010 en el sector censal El Capulí
* P_2022: Población Censo 2022 en el sector censal El Capulí
* NOTA: Ajustar estos valores con la extracción exacta de Redatam

scalar p_2010 = 1250    // Valor de referencia inicial
scalar p_2022 = 1820    // Valor de referencia inicial
scalar t_inter = 12     // Años entre censos (2010 a 2022)

* 2. Cálculo de Tasas de Crecimiento Anual Intercensal
* Tasa geométrica (r_geom): (P_t / P_0)^(1/t) - 1
* Tasa exponencial (r_exp): ln(P_t / P_0) / t

scalar r_geom = (p_2022 / p_2010)^(1 / t_inter) - 1
scalar r_exp  = ln(p_2022 / p_2010) / t_inter

di as result "=========================================================="
di as result " TASA DE CRECIMIENTO INTERCENSAL (EL CAPULÍ):"
di as result " Tasa Geométrica Anual : " %6.4f (scalar(r_geom) * 100) "%"
di as result " Tasa Exponencial Anual: " %6.4f (scalar(r_exp) * 100) "%"
di as result "=========================================================="

* 3. Construcción del dataset de proyección temporal (2022 - 2035)
clear
set obs 14
gen year = 2022 + _n - 1
gen t = year - 2022

* Proyección Exponencial: P(t) = P_2022 * exp(r_exp * t)
gen pob_exponencial = round(scalar(p_2022) * exp(scalar(r_exp) * t))

* Proyección Geométrica: P(t) = P_2022 * (1 + r_geom)^t
gen pob_geometrica  = round(scalar(p_2022) * ((1 + scalar(r_geom))^t))

* 4. Resumen en puntos clave de planificación urbana
list year pob_exponencial pob_geometrica if inlist(year, 2022, 2026, 2030, 2035), sep(0)

* 5. Guardar tabla de proyecciones
export delimited using "`out_dir'/proyecciones_poblacion_el_capuli.csv", replace

* 6. Gráfico de evolución proyectada
twoway (connected pob_exponencial year, lcolor(navy) mcolor(navy) msymbol(circle)) ///
       (connected pob_geometrica year, lcolor(cranberry) mcolor(cranberry) msymbol(diamond) lpattern(dash)), ///
       title("Proyección Demográfica — Barrio El Capulí (2022-2035)") ///
       subtitle("Modelos de Crecimiento Intercensal - UNL Arquitectura / Economía") ///
       ytitle("Población Estimada (Habitantes)") xtitle("Año") ///
       legend(order(1 "Modelo Exponencial" 2 "Modelo Geométrico") ring(0) pos(11)) ///
       scheme(cleanplots)

graph export "`out_dir'/grafico_proyeccion_capuli.png", as(png) replace width(1920)

di as result "Proyección completada y guardada en `out_dir'."
