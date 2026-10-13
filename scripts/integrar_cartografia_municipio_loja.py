import os
import sys
import geopandas as gpd
from shapely.ops import unary_union
from pyproj import Transformer

def procesar_cartografia_completa():
    print("=" * 70)
    print("PROCESAMIENTO CARTOGRÁFICO INTEGRADO — EL CAPULÍ / PUNZARA")
    print("INEC CPV 2022 + CATASTRO MUNICIPAL DE LOJA (EPSG:32717)")
    print("=" * 70)

    base_dir = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v01-diagnostico-territorial-el-capuli\cartografia_qgis"
    raw_muni = r"d:\08_Ciclo\03_Practicas_Preprofesionales\lake\raw\capas_municipio"
    gpkg_loja = os.path.join(base_dir, "11_loja.gpkg")
    gpkg_out = os.path.join(base_dir, "capuli_punzara_estudio.gpkg")

    # 1. Coordenadas y definición del polígono de estudio de El Capulí
    # Ubicación oficial (Colegio San Gerardo / Av. Ruta Éxodo de Yangana / Capulí):
    # Lon: -79.19469, Lat: -4.05242 -> UTM 17S: (700420, 9551855)
    capuli_x, capuli_y = 700420, 9551855
    print(f"\n1. Centro de referencia El Capulí: X={capuli_x}, Y={capuli_y} (UTM 17S)")

    # 2. Cargar Sectores Censales de Loja y definir área de estudio (10 sectores)
    print("\n2. Procesando Sectores Censales del INEC...")
    sec_loja = gpd.read_file(gpkg_loja, layer="sec_a").to_crs(epsg=32717)
    
    # Calcular distancia al centroide de El Capulí y seleccionar los 10 sectores inmediatos
    sec_loja["dist_capuli"] = sec_loja.geometry.distance(gpd.points_from_xy([capuli_x], [capuli_y])[0])
    top10_capuli = sec_loja.sort_values("dist_capuli").head(10).copy()
    top10_capuli["es_estudio_capuli"] = 1
    
    # Unir polígono de los 10 sectores para recorte territorial
    area_estudio_geom = top10_capuli.union_all()
    print(f"   -> 10 Sectores clave de El Capulí identificados:")
    for _, row in top10_capuli.iterrows():
        print(f"      * Sector {row['sec']} (Dist: {row['dist_capuli']:.1f} m)")
    
    # Guardar sectores del área de estudio de El Capulí
    top10_capuli.drop(columns=["dist_capuli"]).to_file(gpkg_out, layer="sectores_estudio_capuli_10", driver="GPKG")
    print(f"   -> Capa 'sectores_estudio_capuli_10' guardada con éxito.")

    # 3. Manzanas Censales (man_a) en el área de estudio
    print("\n3. Procesando Manzanas Censales del INEC en El Capulí...")
    man_loja = gpd.read_file(gpkg_loja, layer="man_a").to_crs(epsg=32717)
    man_capuli = man_loja[man_loja.intersects(area_estudio_geom)].copy()
    man_capuli.to_file(gpkg_out, layer="manzanas_estudio_capuli", driver="GPKG")
    print(f"   -> {len(man_capuli)} Manzanas censales guardadas en 'manzanas_estudio_capuli'.")

    # 4. Edificaciones Censales (edif_p) en el área de estudio
    print("\n4. Procesando Edificaciones Censales del INEC...")
    edif_loja = gpd.read_file(gpkg_loja, layer="edif_p").to_crs(epsg=32717)
    edif_capuli = edif_loja[edif_loja.intersects(area_estudio_geom)].copy()
    edif_capuli.to_file(gpkg_out, layer="edificaciones_estudio_capuli", driver="GPKG")
    print(f"   -> {len(edif_capuli)} Edificaciones censales guardadas en 'edificaciones_estudio_capuli'.")

    # 5. Capas Municipales de Loja: Predios Rurales
    print("\n5. Incorporando Catastro Municipal: Predios Rurales...")
    shp_pr = os.path.join(raw_muni, "PrediosRurales.shp")
    gdf_pr = gpd.read_file(shp_pr, encoding="latin1")
    if gdf_pr.crs is None or gdf_pr.crs.to_epsg() != 32717:
        gdf_pr = gdf_pr.to_crs(epsg=32717)
    pr_capuli = gdf_pr[gdf_pr.intersects(area_estudio_geom)].copy()
    pr_capuli.to_file(gpkg_out, layer="muni_predios_rurales_capuli", driver="GPKG")
    print(f"   -> {len(pr_capuli)} Predios rurales municipales guardados en 'muni_predios_rurales_capuli'.")

    # 6. Capas Municipales de Loja: Predios Urbanos
    print("\n6. Incorporando Catastro Municipal: Predios Urbanos...")
    shp_pu = os.path.join(raw_muni, "PrediosUrbanos.shp")
    gdf_pu = gpd.read_file(shp_pu, encoding="latin1")
    # Los datos vienen en coordenadas UTM 17S (etiquetados erróneamente como EPSG:31992)
    gdf_pu = gdf_pu.set_crs(epsg=32717, allow_override=True)
    pu_capuli = gdf_pu[gdf_pu.intersects(area_estudio_geom)].copy()
    pu_capuli.to_file(gpkg_out, layer="muni_predios_urbanos_capuli", driver="GPKG")
    print(f"   -> {len(pu_capuli)} Predios urbanos municipales guardados en 'muni_predios_urbanos_capuli'.")

    # 7. Capas Municipales de Loja: Construcciones Rurales (Catastro de Bloques)
    print("\n7. Incorporando Catastro Municipal: Construcciones Rurales...")
    shp_cr = os.path.join(raw_muni, "ConstruccionesRurales.shp")
    gdf_cr = gpd.read_file(shp_cr, encoding="latin1")
    if gdf_cr.crs is None or gdf_cr.crs.to_epsg() != 32717:
        gdf_cr = gdf_cr.to_crs(epsg=32717)
    cr_capuli = gdf_cr[gdf_cr.intersects(area_estudio_geom)].copy()
    cr_capuli.to_file(gpkg_out, layer="muni_construcciones_rurales_capuli", driver="GPKG")
    print(f"   -> {len(cr_capuli)} Construcciones rurales guardadas en 'muni_construcciones_rurales_capuli'.")

    # 8. Capas Municipales de Loja: Vialidad Oficial Municipal
    print("\n8. Incorporando Red Vial Municipal de Loja...")
    shp_v = os.path.join(raw_muni, "VIALIDAD_LOJA.shp")
    gdf_v = gpd.read_file(shp_v, encoding="latin1")
    if gdf_v.crs is None or gdf_v.crs.to_epsg() != 32717:
        gdf_v = gdf_v.to_crs(epsg=32717)
    v_capuli = gdf_v[gdf_v.intersects(area_estudio_geom)].copy()
    # Limpiar columnas de texto para evitar errores de codificación
    for col in ["NOMBRE", "JERARQUIA", "RODADURA", "PARROQUIA"]:
        if col in v_capuli.columns:
            v_capuli[col] = v_capuli[col].astype(str).str.encode("ascii", "replace").str.decode("ascii")
    v_capuli.to_file(gpkg_out, layer="muni_vialidad_capuli", driver="GPKG")
    print(f"   -> {len(v_capuli)} Tramos viales municipales guardados en 'muni_vialidad_capuli'.")

    # 9. Capas Municipales de Loja: Estaciones de Bombeo
    print("\n9. Incorporando Estaciones de Bombeo de Loja...")
    shp_eb = os.path.join(raw_muni, "ESTACIONES_BOMBEO.shp")
    gdf_eb = gpd.read_file(shp_eb, encoding="latin1").to_crs(epsg=32717)
    gdf_eb.to_file(gpkg_out, layer="muni_estaciones_bombeo_loja", driver="GPKG")
    print(f"   -> {len(gdf_eb)} Estaciones de bombeo guardadas en 'muni_estaciones_bombeo_loja'.")

    print("\n" + "=" * 70)
    print("TODAS LAS CAPAS FUERON EXTRAÍDAS, RE-PROYECTADAS Y GUARDADAS EN:")
    print(f"{gpkg_out}")
    print("=" * 70)

if __name__ == "__main__":
    procesar_cartografia_completa()
