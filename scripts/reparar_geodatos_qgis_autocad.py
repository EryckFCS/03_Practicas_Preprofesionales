import os
import sys
import geopandas as gpd
from shapely.ops import unary_union

def reparar_y_exportar():
    print("Iniciando procesamiento y estandarización a EPSG:32717...")
    
    base_dir = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v01-diagnostico-territorial-el-capuli\cartografia_qgis"
    gpkg_in = os.path.join(base_dir, "11_loja.gpkg")
    geojson_in = os.path.join(base_dir, "base_maestra_espacial_punzara.geojson")
    
    gpkg_out = os.path.join(base_dir, "capuli_punzara_estudio.gpkg")
    dxf_out = os.path.join(base_dir, "capuli_punzara_autocad.dxf")
    
    # 1. Cargar Base Maestra de Sectores y re-proyectar a EPSG:32717
    print("1. Cargando y re-proyectando sectores censales...")
    gdf_sec = gpd.read_file(geojson_in)
    gdf_sec = gdf_sec.to_crs(epsg=32717)
    gdf_sec.to_file(gpkg_out, layer="sectores_censales_punzara", driver="GPKG")
    print(f"   -> Sectores guardados en {gpkg_out} (Total: {len(gdf_sec)})")
    
    # Obtener envolvente de Punzara
    punzara_geom = unary_union(gdf_sec.geometry)
    
    # 2. Filtrar y re-proyectar Manzanas (man_a)
    print("2. Procesando manzanas censales...")
    gdf_man = gpd.read_file(gpkg_in, layer="man_a")
    gdf_man = gdf_man.to_crs(epsg=32717)
    # Filtrar por código de Punzara (110156) o por intersección espacial
    gdf_man_punzara = gdf_man[gdf_man["man"].astype(str).str.startswith("110156")].copy()
    if len(gdf_man_punzara) == 0:
        gdf_man_punzara = gdf_man[gdf_man.intersects(punzara_geom)].copy()
    gdf_man_punzara.to_file(gpkg_out, layer="manzanas_punzara", driver="GPKG")
    print(f"   -> Manzanas guardadas (Total: {len(gdf_man_punzara)})")
    
    # 3. Filtrar y re-proyectar Ejes Viales (ejes_l)
    print("3. Procesando red vial y calles...")
    gdf_ejes = gpd.read_file(gpkg_in, layer="ejes_l")
    gdf_ejes = gdf_ejes.to_crs(epsg=32717)
    gdf_ejes_punzara = gdf_ejes[gdf_ejes.intersects(punzara_geom)].copy()
    gdf_ejes_punzara.to_file(gpkg_out, layer="vias_calles_punzara", driver="GPKG")
    print(f"   -> Vías guardadas (Total: {len(gdf_ejes_punzara)})")
    
    # 4. Filtrar y re-proyectar Edificaciones (edif_p)
    print("4. Procesando edificaciones prediales...")
    gdf_edif = gpd.read_file(gpkg_in, layer="edif_p")
    gdf_edif = gdf_edif.to_crs(epsg=32717)
    gdf_edif_punzara = gdf_edif[gdf_edif.intersects(punzara_geom)].copy()
    gdf_edif_punzara.to_file(gpkg_out, layer="edificaciones_punzara", driver="GPKG")
    print(f"   -> Edificaciones guardadas (Total: {len(gdf_edif_punzara)})")
    
    # 5. Exportar a DXF para AutoCAD
    print("5. Exportando capas vectoriales a AutoCAD DXF...")
    # Creamos un shapefile o DXF combinado
    # En QGIS/GDAL, podemos guardar las manzanas y vías en DXF
    try:
        # Exportar vías y manzanas a DXF usando GDAL/OGR
        from osgeo import ogr, osr
        driver_dxf = ogr.GetDriverByName("DXF")
        if os.path.exists(dxf_out):
            os.remove(dxf_out)
        ds_dxf = driver_dxf.CreateDataSource(dxf_out)
        
        # Capa Manzanas
        layer_man_dxf = ds_dxf.CreateLayer("MANZANAS", geom_type=ogr.wkbMultiPolygon)
        for _, row in gdf_man_punzara.iterrows():
            feat = ogr.Feature(layer_man_dxf.GetLayerDefn())
            feat.SetGeometry(ogr.CreateGeometryFromWkt(row.geometry.wkt))
            layer_man_dxf.CreateFeature(feat)
            
        # Capa Vías
        layer_vias_dxf = ds_dxf.CreateLayer("VIAS", geom_type=ogr.wkbMultiLineString)
        for _, row in gdf_ejes_punzara.iterrows():
            feat = ogr.Feature(layer_vias_dxf.GetLayerDefn())
            feat.SetGeometry(ogr.CreateGeometryFromWkt(row.geometry.wkt))
            layer_vias_dxf.CreateFeature(feat)
            
        ds_dxf = None
        print(f"   -> Archivo DXF para AutoCAD generado con éxito en: {dxf_out}")
    except Exception as e:
        print(f"   Aviso en exportación DXF OGR: {e}")
        # Fallback con geopandas a DXF o Shapefile para AutoCAD
        gdf_man_punzara.to_file(os.path.join(base_dir, "manzanas_autocad.shp"))
        gdf_ejes_punzara.to_file(os.path.join(base_dir, "vias_autocad.shp"))
        print("   -> Capas exportadas también como Shapefiles compatibles con AutoCAD MAP/Civil 3D.")
        
    print("Estandarización completada con éxito.")

if __name__ == "__main__":
    reparar_y_exportar()
