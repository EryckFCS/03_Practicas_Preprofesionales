"""Calcula modelos de proyección demográfica (geométrico y exponencial) para Punzara / El Capulí."""

from __future__ import annotations

import math
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def compute_projections() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    evidencias_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "evidencias"
    data_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "datos_redatam"
    evidencias_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================================")
    print(" MODELOS DE PROYECCIÓN DEMOGRÁFICA: PUNZARA / EL CAPULÍ")
    print("==================================================================")

    # Población base oficial censal
    p_2010 = 6845  # Censo 2010 INEC (Punzara)
    p_2022 = 8669  # Censo 2022 INEC (Punzara)
    t_inter = 12.0 # Años entre censos (2010-2022)

    # Tasas de crecimiento intercensal
    r_geom = (p_2022 / p_2010) ** (1.0 / t_inter) - 1.0
    r_exp = math.log(p_2022 / p_2010) / t_inter

    print(f"Población Censo 2010: {p_2010:,} habitantes")
    print(f"Población Censo 2022: {p_2022:,} habitantes")
    print(f"Tasa geométrica anual : {r_geom * 100:.3f}% anual")
    print(f"Tasa exponencial anual: {r_exp * 100:.3f}% anual\n")

    years = list(range(2022, 2036))
    records = []

    for y in years:
        t = float(y - 2022)
        pob_geom = round(p_2022 * ((1.0 + r_geom) ** t))
        pob_exp = round(p_2022 * math.exp(r_exp * t))
        records.append({
            "anio": y,
            "horizonte_t": int(t),
            "poblacion_geometrica": pob_geom,
            "poblacion_exponencial": pob_exp,
        })

    df_proj = pd.DataFrame(records)
    out_csv = data_dir / "proyecciones_poblacion_capuli.csv"
    df_proj.to_csv(out_csv, index=False)
    print(f"[+] Tabla de proyecciones guardada: {out_csv.name}")

    # Puntos clave de planificación
    print("\nHorizontes clave de planificación urbana:")
    for yr in [2022, 2026, 2030, 2035]:
        row = df_proj[df_proj["anio"] == yr].iloc[0]
        print(f"  • Año {yr}: {row['poblacion_geometrica']:,} hab. (Geom) | {row['poblacion_exponencial']:,} hab. (Exp)")

    # Gráfico de Proyección
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    ax.plot(
        df_proj["anio"],
        df_proj["poblacion_geometrica"],
        marker="o",
        color="#1d3557",
        linewidth=2.2,
        label=f"Modelo Geométrico (r = {r_geom*100:.2f}%)",
    )
    ax.plot(
        df_proj["anio"],
        df_proj["poblacion_exponencial"],
        marker="s",
        linestyle="--",
        color="#e63946",
        linewidth=2.0,
        label=f"Modelo Exponencial (r = {r_exp*100:.2f}%)",
    )

    # Anotar puntos clave
    for yr in [2022, 2026, 2030, 2035]:
        p = df_proj[df_proj["anio"] == yr]["poblacion_geometrica"].values[0]
        ax.annotate(
            f"{p:,} hab.",
            xy=(yr, p),
            xytext=(yr, p + 140),
            ha="center",
            fontsize=8.5,
            fontweight="bold",
            color="#1d3557",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#f1faee", edgecolor="#457b9d", alpha=0.9),
        )

    ax.set_title(
        "Proyecciones Demográficas — Parroquia Punzara / Barrio El Capulí (2022–2035)\nCarrera de Economía & Carrera de Arquitectura Sostenible (UNL)",
        fontsize=11,
        fontweight="bold",
        pad=15,
        color="#1d3557",
    )
    ax.set_xlabel("Año de Planificación", fontsize=9.5, fontweight="bold", color="#333333")
    ax.set_ylabel("Población Proyectada (Habitantes)", fontsize=9.5, fontweight="bold", color="#333333")
    ax.set_ylim(8200, 12000)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc")

    plt.tight_layout()
    chart_file = evidencias_dir / "grafico_proyeccion_capuli.png"
    plt.savefig(chart_file, dpi=300)
    plt.close()
    print(f"[+] Gráfico de proyecciones generado: {chart_file.name}")
    print("==================================================================")


if __name__ == "__main__":
    compute_projections()
