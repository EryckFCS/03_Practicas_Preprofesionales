"""Intersección Barrio ∩ Sector Censal INEC y ponderación dasimétrica por edificaciones edif_p."""

from __future__ import annotations

import copy
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.ops import unary_union


BASE_DIR = Path(
    r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\03_encuesta_barrio_capuli"
)


def main() -> None:
    g11 = BASE_DIR.parent.parent / "v01-diagnostico-territorial-el-capuli" / "cartografia_qgis" / "11_loja.gpkg"
    main_dir = BASE_DIR / "qgis" / "01_proyecto_principal"
    gpkg_main = main_dir / "proyecto_principal_capuli_y_periurbano.gpkg"
    qgz_main = main_dir / "proyecto_principal_capuli_y_periurbano.qgz"

    # 1. Consolidar las 27 unidades operativas: 9 sectores Capulí + ZII-01 + 17 sectores periurbanos
    sec9 = gpd.read_file(gpkg_main, layer="00_sectores_internos_capuli_9").to_crs(32717)
    zii = gpd.read_file(gpkg_main, layer="00h_zona_influencia_indirecta_capuli").to_crs(32717)
    pu17 = gpd.read_file(gpkg_main, layer="00i_sectores_periurbano_capuli").to_crs(32717)

    units_rows = []
    for _, r in sec9.iterrows():
        units_rows.append({"unidad_cod": str(r["sector_cod"]), "unidad_nombre": str(r["nombre_sector"]), "ambito": "BARRIO_CAPULI", "geometry": r.geometry})
    for _, r in zii.iterrows():
        units_rows.append({"unidad_cod": str(r["zona_cod"]), "unidad_nombre": str(r["nombre_zona"]), "ambito": "INFLUENCIA_INDIRECTA", "geometry": r.geometry})
    for _, r in pu17.iterrows():
        units_rows.append({"unidad_cod": str(r["sector_pu_cod"]), "unidad_nombre": str(r["nombre_sector_pu"]), "ambito": "PERIURBANO_SUR", "geometry": r.geometry})
    units = gpd.GeoDataFrame(units_rows, crs=32717)

    # 2. Cargar sectores censales oficiales sec_a y edificaciones edif_p de 11_loja.gpkg
    sec_a = gpd.read_file(g11, layer="sec_a", bbox=tuple(units.total_bounds)).to_crs(32717)
    sec_a = sec_a[sec_a.geometry.intersects(units.geometry.union_all())].copy().reset_index(drop=True)

    ed_all = gpd.read_file(g11, layer="edif_p", bbox=tuple(sec_a.total_bounds)).to_crs(32717)
    ed_all["geometry"] = ed_all.geometry.centroid
    ed_res = ed_all[ed_all["cod_otros"].isna()].copy()

    # Conteo N_sector de viviendas residenciales edif_p por cada sector censal oficial completo
    sec_totals: dict[str, int] = {}
    for _, sr in sec_a.iterrows():
        scod = str(sr["sec"])
        n_sec = int(ed_res.geometry.within(sr.geometry.buffer(0.5)).sum())
        sec_totals[scod] = n_sec

    # 3. Intersección Barrio ∩ Sector Censal y cálculo de peso dasimétrico w = n_barrio_sector / N_sector
    inter_rows = []
    for _, ur in units.iterrows():
        ug = ur.geometry.buffer(0)
        for _, sr in sec_a.iterrows():
            scod = str(sr["sec"])
            sg = sr.geometry.buffer(0)
            if not ug.intersects(sg):
                continue
            ig = ug.intersection(sg).buffer(0)
            if ig.is_empty or ig.area < 50.0:
                continue
            n_sub = int(ed_res.geometry.within(ig.buffer(0.5)).sum())
            n_tot_sec = sec_totals.get(scod, 0)
            if n_sub == 0 and ig.area < 5000.0:
                continue
            w = round(n_sub / n_tot_sec, 4) if n_tot_sec > 0 else 0.0
            area_ha = round(float(ig.area / 1e4), 2)
            inter_rows.append({
                "sub_cod": f"{ur['unidad_cod']}_{scod[-6:]}",
                "unidad_cod": ur["unidad_cod"],
                "unidad_nombre": ur["unidad_nombre"],
                "ambito": ur["ambito"],
                "sec_inec": scod,
                "area_ha": area_ha,
                "n_viv_interseccion": n_sub,
                "n_viv_sector_inec": n_tot_sec,
                "peso_dasimetrico_w": w,
                "pct_sector_inec": round(w * 100.0, 2),
                "geometry": ig,
            })

    gdf_inter = gpd.GeoDataFrame(inter_rows, crs=32717).sort_values(["ambito", "unidad_cod", "sec_inec"]).reset_index(drop=True)

    # 4. Guardar capa espacial en el GeoPackage principal y exportar CSV + Excel
    gdf_inter.to_file(gpkg_main, layer="00j_barrios_por_sector_censal_inec", driver="GPKG")

    df_mat = pd.DataFrame(gdf_inter.drop(columns=["geometry"]))
    csv_out = main_dir / "matriz_barrio_sector_censal_pesos_edif.csv"
    df_mat.to_csv(csv_out, index=False, encoding="utf-8-sig")

    xlsx_out = main_dir / "matriz_barrio_sector_censal_pesos_edif.xlsx"
    df_sec_sum = df_mat.groupby("sec_inec", as_index=False).agg(
        unidades_intersectadas=("unidad_cod", "nunique"),
        area_cubierta_ha=("area_ha", "sum"),
        viv_en_unidades=("n_viv_interseccion", "sum"),
        viv_totales_sector_inec=("n_viv_sector_inec", "first"),
        suma_pesos_w=("peso_dasimetrico_w", "sum"),
    )
    df_sec_sum["pct_cubierto_sector"] = (df_sec_sum["suma_pesos_w"] * 100.0).round(2)
    with pd.ExcelWriter(xlsx_out, engine="openpyxl") as writer:
        df_mat.to_excel(writer, sheet_name="Matriz_Barrio_x_Sector_INEC", index=False)
        df_sec_sum.to_excel(writer, sheet_name="Resumen_por_Sector_INEC", index=False)

    # 5. Agregar capa 00j_barrios_por_sector_censal_inec al proyecto QGIS principal (desactivada por defecto)
    with zipfile.ZipFile(qgz_main, "r") as zf:
        files = {n: zf.read(n) for n in zf.namelist()}
    qgs_name = [n for n in files if n.endswith(".qgs")][0]
    root = ET.fromstring(files[qgs_name])
    proj_layers = root.find("projectlayers")
    new_id = "barrios_por_sector_censal_inec_00j"
    template_ml = None
    for ml in list(proj_layers.findall("maplayer")):
        lid = ml.find("id")
        if lid is not None and lid.text == new_id:
            proj_layers.remove(ml)
        elif lid is not None and lid.text == "zii_01_influencia_indirecta":
            template_ml = ml
    if template_ml is not None:
        nml = copy.deepcopy(template_ml)
        nml.find("id").text = new_id
        nml.find("layername").text = f"Encaje Barrio x Sector Censal INEC · {len(gdf_inter)} subpolígonos"
        nml.find("datasource").text = "./proyecto_principal_capuli_y_periurbano.gpkg|layername=00j_barrios_por_sector_censal_inec"
        for opt in nml.findall(".//Option"):
            if opt.get("name") == "color": opt.set("value", "14,165,233,35")
            elif opt.get("name") == "outline_color": opt.set("value", "248,250,252,220")
            elif opt.get("name") == "outline_style": opt.set("value", "dash")
            elif opt.get("name") == "outline_width": opt.set("value", "0.55")
        proj_layers.append(nml)
    ltg = root.find("layer-tree-group")
    if ltg is not None:
        for ch in list(ltg.findall(".//layer-tree-layer")):
            if ch.get("id") == new_id:
                ltg.remove(ch)
        ltg.insert(0, ET.Element("layer-tree-layer", {
            "id": new_id,
            "name": f"Encaje Barrio x Sector Censal INEC · {len(gdf_inter)} subpolígonos",
            "checked": "Qt::Unchecked",
            "expanded": "1",
            "source": "./proyecto_principal_capuli_y_periurbano.gpkg|layername=00j_barrios_por_sector_censal_inec",
            "providerKey": "ogr",
        }))
    files[qgs_name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(qgz_main, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for n, data in files.items(): zf.writestr(n, data)

    # 6. Mapa diagnóstico
    fig, ax = plt.subplots(figsize=(12.5, 9.5), dpi=170, facecolor="#0f172a")
    ax.set_facecolor("#1e293b")
    sec_a.plot(ax=ax, facecolor="none", edgecolor="#94a3b8", linestyle="--", linewidth=1.1, alpha=0.8)
    gdf_inter.plot(ax=ax, column="sec_inec", cmap="tab20", alpha=0.55, edgecolor="#f8fafc", linewidth=0.9)
    for _, sr in sec_a.iterrows():
        pt = sr.geometry.representative_point()
        ax.annotate(str(sr["sec"])[-6:], xy=(pt.x, pt.y), ha="center", va="center", color="#facc15", fontsize=8, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.14", facecolor="#0f172a", edgecolor="#facc15", alpha=0.75))
    ax.set_title(f"Encaje Barrio ∩ Sector Censal INEC · {len(gdf_inter)} subpolígonos · {len(sec_a)} sectores INEC", color="#f8fafc", fontsize=12.5, fontweight="bold")
    ax.tick_params(colors="#94a3b8", labelsize=8)
    plt.tight_layout()
    fig.savefig(BASE_DIR / "assets" / "mapa_encaje_barrios_sectores_censales.png", dpi=170, facecolor="#0f172a")
    plt.close(fig)

    print(f"Subpolígonos generados: {len(gdf_inter)} · Sectores INEC intersectados: {len(sec_a)}")
    print(f"Total viviendas edif_p asignadas: {int(df_mat['n_viv_interseccion'].sum())}")
    print("--- Resumen por Sector Censal INEC ---")
    print(df_sec_sum.to_string(index=False))


if __name__ == "__main__":
    main()
