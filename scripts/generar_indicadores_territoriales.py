"""Genera la matriz de indicadores censales a nivel de sector para el Cantón Loja y Punzara."""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def generate_indicators() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "datos_redatam"

    pob_csv = data_dir / "cpv2022_loja_poblacion_sector.csv"
    viv_csv = data_dir / "cpv2022_loja_vivienda_sector.csv"
    hog_csv = data_dir / "cpv2022_loja_hogar_sector.csv"

    print("==================================================================")
    print(" GENERACIÓN DE INDICADORES TERRITORIALES: CENSO 2022 (LOJA)")
    print("==================================================================")

    # 1. Procesar Población
    print("[*] Procesando microdatos de población...")
    df_pob = pd.read_csv(pob_csv, usecols=["I01", "I02", "I03", "I04", "I05", "P02", "P03"])
    df_pob["id_sec"] = (
        df_pob["I01"].astype(str).str.zfill(2)
        + df_pob["I02"].astype(str).str.zfill(2)
        + df_pob["I03"].astype(str).str.zfill(2)
        + df_pob["I04"].astype(str).str.zfill(3)
        + df_pob["I05"].astype(str).str.zfill(3)
    )

    agg_pob = (
        df_pob.groupby("id_sec")
        .agg(
            poblacion_total=("P02", "count"),
            hombres=("P02", lambda x: (x == 1).sum()),
            mujeres=("P02", lambda x: (x == 2).sum()),
            pob_0_14=("P03", lambda x: (x < 15).sum()),
            pob_15_64=("P03", lambda x: ((x >= 15) & (x <= 64)).sum()),
            pob_65_mas=("P03", lambda x: (x >= 65).sum()),
            edad_promedio=("P03", "mean"),
        )
        .reset_index()
    )
    agg_pob["indice_dependencia"] = (
        (agg_pob["pob_0_14"] + agg_pob["pob_65_mas"]) / agg_pob["pob_15_64"].replace(0, pd.NA) * 100
    ).round(2)
    agg_pob["edad_promedio"] = agg_pob["edad_promedio"].round(1)

    # 2. Procesar Vivienda
    print("[*] Procesando microdatos de vivienda...")
    df_viv = pd.read_csv(viv_csv, usecols=["I01", "I02", "I03", "I04", "I05", "V01", "V06", "V09", "V11", "V12"])
    df_viv["id_sec"] = (
        df_viv["I01"].astype(str).str.zfill(2)
        + df_viv["I02"].astype(str).str.zfill(2)
        + df_viv["I03"].astype(str).str.zfill(2)
        + df_viv["I04"].astype(str).str.zfill(3)
        + df_viv["I05"].astype(str).str.zfill(3)
    )

    agg_viv = (
        df_viv.groupby("id_sec")
        .agg(
            total_viviendas=("V01", "count"),
            pct_agua_red=("V06", lambda x: ((x == 1).sum() / len(x) * 100).round(1)),
            pct_alcantarillado=("V09", lambda x: ((x == 1).sum() / len(x) * 100).round(1)),
            pct_luz_electrica=("V11", lambda x: ((x == 1).sum() / len(x) * 100).round(1)),
            pct_recoleccion_basura=("V12", lambda x: ((x == 1).sum() / len(x) * 100).round(1)),
        )
        .reset_index()
    )

    # 3. Procesar Hogar
    print("[*] Procesando microdatos de hogar...")
    df_hog = pd.read_csv(hog_csv, usecols=["I01", "I02", "I03", "I04", "I05", "H02", "H0701", "H0702", "H0703"])
    df_hog["id_sec"] = (
        df_hog["I01"].astype(str).str.zfill(2)
        + df_hog["I02"].astype(str).str.zfill(2)
        + df_hog["I03"].astype(str).str.zfill(2)
        + df_hog["I04"].astype(str).str.zfill(3)
        + df_hog["I05"].astype(str).str.zfill(3)
    )

    agg_hog = (
        df_hog.groupby("id_sec")
        .agg(
            total_hogares=("H02", "count"),
            dormitorios_promedio=("H02", "mean"),
            pct_nbi_pobreza=("H0701", lambda x: ((x == 1).sum() / len(x) * 100).round(1)),
        )
        .reset_index()
    )
    agg_hog["dormitorios_promedio"] = agg_hog["dormitorios_promedio"].round(2)

    # 4. Consolidar Matriz
    print("[*] Integrando matriz maestra de indicadores...")
    df_merged = agg_pob.merge(agg_viv, on="id_sec", how="left").merge(agg_hog, on="id_sec", how="left")
    df_merged["parroquia"] = df_merged["id_sec"].str.slice(0, 6)

    # Guardar Cantón Loja
    out_loja = data_dir / "cpv2022_loja_indicadores_sectores.csv"
    df_merged.to_csv(out_loja, index=False)
    print(f"[+] Generado: {out_loja.name} ({len(df_merged)} sectores censales)")

    # Guardar Subconjunto Punzara (110156)
    out_punzara = data_dir / "cpv2022_punzara_indicadores_sectores.csv"
    df_punzara = df_merged[df_merged["parroquia"] == "110156"].copy()
    df_punzara.to_csv(out_punzara, index=False)
    print(f"[+] Generado: {out_punzara.name} ({len(df_punzara)} sectores de Punzara)")

    print("\nResumen demográfico de Punzara:")
    print(f"  • Población total censada: {df_punzara['poblacion_total'].sum():,} habitantes")
    print(f"  • Hombres: {df_punzara['hombres'].sum():,} | Mujeres: {df_punzara['mujeres'].sum():,}")
    print(f"  • Viviendas totales: {df_punzara['total_viviendas'].sum():,}")
    print(f"  • Hogares totales: {df_punzara['total_hogares'].sum():,}")
    print(f"  • Cobertura promedio agua potable: {df_punzara['pct_agua_red'].mean():.1f}%")
    print(f"  • Cobertura promedio alcantarillado: {df_punzara['pct_alcantarillado'].mean():.1f}%")
    print("==================================================================")


if __name__ == "__main__":
    generate_indicators()
