"""Construye la base maestra espacial con coordenadas fusionadas y genera los mapas temáticos."""

from __future__ import annotations

from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch


def build_spatial_master() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    gpkg_path = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "cartografia_qgis" / "11_loja.gpkg"
    data_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "datos_redatam"
    evidencias_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "evidencias"
    cartografia_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "cartografia_qgis"
    evidencias_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================================")
    print(" 1. FUSIÓN ESPACIAL: CARTOGRAFÍA + VARIABLES CENSALES 2022")
    print("==================================================================")

    # 1. Cargar capa vectorial de sectores censales
    print("[*] Leyendo sectores censales desde 11_loja.gpkg (sec_a)...")
    gdf_sec = gpd.read_file(gpkg_path, layer="sec_a")
    
    # Filtrar sectores de Punzara (110156)
    gdf_punzara = gdf_sec[gdf_sec["sec"].astype(str).str.startswith("110156")].copy()
    print(f"  [+] Sectores de Punzara encontrados en cartografía: {len(gdf_punzara)}")

    # 2. Cargar tabla de indicadores censales
    csv_indicadores = data_dir / "cpv2022_punzara_indicadores_sectores.csv"
    df_ind = pd.read_csv(csv_indicadores)
    df_ind["id_sec"] = df_ind["id_sec"].astype(str)
    gdf_punzara["sec"] = gdf_punzara["sec"].astype(str)

    # 3. Merge espacial
    gdf_master = gdf_punzara.merge(df_ind, left_on="sec", right_on="id_sec", how="inner")
    print(f"  [+] Sectores fusionados con datos censales: {len(gdf_master)}")

    # 4. Cálculo de Métricas Espaciales y Coordenadas
    # Asegurar proyección métrica (EPSG:31992 o UTM 17S EPSG:32717)
    if gdf_master.crs is None or gdf_master.crs.to_epsg() != 32717:
        gdf_master = gdf_master.to_crs(epsg=32717)

    # Superficie
    gdf_master["area_m2"] = gdf_master.geometry.area
    gdf_master["area_ha"] = (gdf_master["area_m2"] / 10000.0).round(2)
    gdf_master["area_km2"] = (gdf_master["area_m2"] / 1000000.0).round(4)
    gdf_master["densidad_hab_km2"] = (
        gdf_master["poblacion_total"] / gdf_master["area_km2"].replace(0, pd.NA)
    ).round(1)

    # Coordenadas UTM (Centroide)
    centroids_utm = gdf_master.geometry.centroid
    gdf_master["coord_utm_x"] = centroids_utm.x.round(2)
    gdf_master["coord_utm_y"] = centroids_utm.y.round(2)

    # Coordenadas Geográficas WGS84 (Latitud / Longitud)
    gdf_wgs84 = gdf_master.to_crs(epsg=4326)
    centroids_wgs84 = gdf_wgs84.geometry.centroid
    gdf_master["longitud_wgs84"] = centroids_wgs84.x.round(6)
    gdf_master["latitud_wgs84"] = centroids_wgs84.y.round(6)

    # 5. Exportar Base Maestra Espacial
    out_csv = data_dir / "base_maestra_espacial_punzara.csv"
    # Guardar CSV plano sin columna geométrica cruda
    df_export = gdf_master.drop(columns=["geometry"])
    df_export.to_csv(out_csv, index=False)
    print(f"[+] Base maestra exportada en CSV: {out_csv.name} ({len(df_export)} registros)")

    out_geojson = cartografia_dir / "base_maestra_espacial_punzara.geojson"
    gdf_wgs84_export = gdf_master.to_crs(epsg=4326)
    gdf_wgs84_export.to_file(out_geojson, driver="GeoJSON")
    print(f"[+] Capa espacial GeoJSON lista para QGIS: {out_geojson.name}")

    print("\n==================================================================")
    print(" 2. RENDERIZADO DE MAPAS TEMÁTICOS DE ALTA RESOLUCIÓN")
    print("==================================================================")

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # MAPA 1: DENSIDAD POBLACIONAL POR SECTOR
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    gdf_plot = gdf_master.copy()
    gdf_plot["densidad_hab_km2"] = gdf_plot["densidad_hab_km2"].fillna(0)

    gdf_plot.plot(
        column="densidad_hab_km2",
        cmap="YlOrRd",
        linewidth=0.6,
        edgecolor="#4a5568",
        legend=True,
        legend_kwds={
            "label": "Densidad Poblacional (Habitantes / km²)",
            "orientation": "horizontal",
            "shrink": 0.7,
            "pad": 0.05,
        },
        ax=ax,
    )

    ax.set_title(
        "Densidad Poblacional por Sector Censal — Parroquia Punzara (El Capulí)\nCenso de Población y Vivienda 2022 (INEC)",
        fontsize=12,
        fontweight="bold",
        pad=15,
        color="#1a365d",
    )
    ax.set_xlabel("Coordenada Este UTM (m)", fontsize=9, color="#4a5568")
    ax.set_ylabel("Coordenada Norte UTM (m)", fontsize=9, color="#4a5568")

    # Flecha Norte
    ax.annotate(
        "N",
        xy=(0.95, 0.90),
        xytext=(0.95, 0.82),
        xycoords="axes fraction",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#1a365d",
        arrowprops=dict(facecolor="#1a365d", width=2, headwidth=8),
    )

    map_densidad_file = evidencias_dir / "mapa_densidad_poblacional_punzara.png"
    plt.tight_layout()
    plt.savefig(map_densidad_file, dpi=300)
    plt.close()
    print(f"[+] Mapa de densidad generado: {map_densidad_file.name}")

    # MAPA 2: DÉFICIT DE COBERTURA DE AGUA POTABLE (100 - pct_agua_red)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    gdf_plot["deficit_agua"] = 100.0 - gdf_plot["pct_agua_red"].fillna(0)

    gdf_plot.plot(
        column="deficit_agua",
        cmap="Reds",
        linewidth=0.6,
        edgecolor="#2d3748",
        legend=True,
        legend_kwds={
            "label": "Déficit de Cobertura de Agua Potable por Red (%)",
            "orientation": "horizontal",
            "shrink": 0.7,
            "pad": 0.05,
        },
        ax=ax,
    )

    ax.set_title(
        "Déficit de Cobertura de Agua Potable — Parroquia Punzara / El Capulí\nDiagnóstico de Infraestructura Básica (UNL Arquitectura & Economía)",
        fontsize=12,
        fontweight="bold",
        pad=15,
        color="#742a2a",
    )
    ax.set_xlabel("Coordenada Este UTM (m)", fontsize=9, color="#4a5568")
    ax.set_ylabel("Coordenada Norte UTM (m)", fontsize=9, color="#4a5568")

    # Flecha Norte
    ax.annotate(
        "N",
        xy=(0.95, 0.90),
        xytext=(0.95, 0.82),
        xycoords="axes fraction",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#742a2a",
        arrowprops=dict(facecolor="#742a2a", width=2, headwidth=8),
    )

    map_agua_file = evidencias_dir / "mapa_deficit_agua_punzara.png"
    plt.tight_layout()
    plt.savefig(map_agua_file, dpi=300)
    plt.close()
    print(f"[+] Mapa de déficit hidrosanitario generado: {map_agua_file.name}")

    print("==================================================================")
    print(" Proceso espacial completado exitosamente.")
    print("==================================================================")


if __name__ == "__main__":
    build_spatial_master()
