import os
import sys

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsGraduatedSymbolRenderer,
    QgsSingleSymbolRenderer,
    QgsRendererRange,
    QgsSymbol,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer
)
from PyQt5.QtGui import QColor

def build_qgis_project():
    print("Iniciando generación de proyecto QGIS...")
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    project = QgsProject.instance()
    project.clear()
    project.setTitle("Diagnóstico Territorial y Poblacional — Barrio El Capulí (Punzara, Loja)")
    
    # CRS EPSG:32717 (WGS 84 / UTM Zone 17S)
    crs = QgsCoordinateReferenceSystem("EPSG:32717")
    project.setCrs(crs)
    
    base_dir = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v01-diagnostico-territorial-el-capuli\cartografia_qgis"
    gpkg_path = os.path.join(base_dir, "11_loja.gpkg")
    geojson_path = os.path.join(base_dir, "base_maestra_espacial_punzara.geojson")
    output_qgz = os.path.join(base_dir, "proyecto_diagnostico_capuli.qgz")
    
    root = project.layerTreeRoot()
    group_diagnostico = root.addGroup("1. Indicadores Territoriales (CPV 2022)")
    group_carto_base = root.addGroup("2. Cartografía Urbana INEC (Loja/Punzara)")
    group_mapas_web = root.addGroup("3. Mapa Base Satelital / Callejero")
    
    # 1. Capa GeoJSON Base Maestra Punzara
    print("Cargando Capa Base Maestra Punzara...")
    vl_punzara = QgsVectorLayer(geojson_path, "Sectores Censales — Punzara (Densidad Pob)", "ogr")
    if vl_punzara.isValid():
        ranges = []
        color_palette = [
            (0, 50, "#fee5d9", "Muy Baja (< 50 hab/km²)"),
            (50, 150, "#fcae91", "Baja (50 - 150 hab/km²)"),
            (150, 300, "#fb6a4a", "Media (150 - 300 hab/km²)"),
            (300, 600, "#de2d26", "Alta (300 - 600 hab/km²)"),
            (600, 99999, "#a50f15", "Muy Alta (> 600 hab/km²)")
        ]
        for lower, upper, color_hex, label in color_palette:
            sym = QgsSymbol.defaultSymbol(vl_punzara.geometryType())
            fill_layer = sym.symbolLayer(0)
            if fill_layer:
                fill_layer.setColor(QColor(color_hex))
                fill_layer.setStrokeColor(QColor("#2c3e50"))
                fill_layer.setStrokeWidth(0.3)
            sym.setOpacity(0.8)
            ranges.append(QgsRendererRange(lower, upper, sym, label))
            
        renderer = QgsGraduatedSymbolRenderer("densidad_hab_km2", ranges)
        vl_punzara.setRenderer(renderer)
        project.addMapLayer(vl_punzara, False)
        group_diagnostico.addLayer(vl_punzara)
        print("Capa Punzara añadida con éxito.")
    else:
        print("Error: No se pudo cargar GeoJSON de Punzara.")

    # 2. Capa Manzanas Censales (man_a)
    print("Cargando Manzanas Censales...")
    vl_man = QgsVectorLayer(f"{gpkg_path}|layername=man_a", "Manzanas Censales (INEC)", "ogr")
    if vl_man.isValid():
        vl_man.setSubsetString("man LIKE '110156%'")
        sym_man = QgsSymbol.defaultSymbol(vl_man.geometryType())
        fill_l = sym_man.symbolLayer(0)
        if fill_l:
            fill_l.setColor(QColor(0, 0, 0, 0)) # Transparente
            fill_l.setStrokeColor(QColor("#d35400")) # Borde naranja
            fill_l.setStrokeWidth(0.4)
        vl_man.setRenderer(QgsSingleSymbolRenderer(sym_man))
        project.addMapLayer(vl_man, False)
        group_carto_base.addLayer(vl_man)
        print(f"Manzanas cargadas (total filtrado: {vl_man.featureCount()}).")

    # 3. Capa Ejes Viales (ejes_l)
    print("Cargando Ejes Viales...")
    vl_ejes = QgsVectorLayer(f"{gpkg_path}|layername=ejes_l", "Ejes Viales / Calles (INEC)", "ogr")
    if vl_ejes.isValid():
        sym_ejes = QgsSymbol.defaultSymbol(vl_ejes.geometryType())
        line_l = sym_ejes.symbolLayer(0)
        if line_l:
            line_l.setColor(QColor("#7f8c8d"))
            line_l.setWidth(0.3)
        vl_ejes.setRenderer(QgsSingleSymbolRenderer(sym_ejes))
        project.addMapLayer(vl_ejes, False)
        group_carto_base.addLayer(vl_ejes)
        print("Ejes viales cargados.")

    # 4. Capa Edificaciones (edif_p)
    print("Cargando Edificaciones...")
    vl_edif = QgsVectorLayer(f"{gpkg_path}|layername=edif_p", "Edificaciones / Predios (Puntos INEC)", "ogr")
    if vl_edif.isValid():
        sym_edif = QgsSymbol.defaultSymbol(vl_edif.geometryType())
        marker_l = sym_edif.symbolLayer(0)
        if marker_l:
            marker_l.setColor(QColor("#2980b9"))
            marker_l.setSize(1.2)
            marker_l.setStrokeColor(QColor("#ffffff"))
            marker_l.setStrokeWidth(0.2)
        vl_edif.setRenderer(QgsSingleSymbolRenderer(sym_edif))
        project.addMapLayer(vl_edif, False)
        node_edif = group_carto_base.addLayer(vl_edif)
        node_edif.setItemVisibilityChecked(False) # Apagada inicialmente
        print("Edificaciones añadidas (visibilidad inicial: desactivada).")

    # 5. Capa OpenStreetMap XYZ
    print("Añadiendo Capa Base OpenStreetMap...")
    osm_uri = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
    rl_osm = QgsRasterLayer(osm_uri, "OpenStreetMap Estándar", "wms")
    if rl_osm.isValid():
        project.addMapLayer(rl_osm, False)
        group_mapas_web.addLayer(rl_osm)
        print("OpenStreetMap añadido.")
    else:
        print("Aviso: No se pudo inicializar OpenStreetMap XYZ.")

    # Guardar proyecto
    print(f"Guardando proyecto en: {output_qgz}")
    success = project.write(output_qgz)
    print("Proyecto guardado con éxito:", success)
    
    qgs.exitQgis()
    print("Finalizado con éxito.")

if __name__ == "__main__":
    build_qgis_project()
