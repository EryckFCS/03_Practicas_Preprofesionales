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
    QgsRectangle,
    QgsReferencedRectangle,
    QgsDxfExport
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QFile, QIODevice

def construir_todo():
    print("Iniciando generación de proyecto QGIS y DXF para AutoCAD...")
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    project = QgsProject.instance()
    project.clear()
    project.setTitle("Diagnóstico Territorial y Poblacional — Barrio El Capulí (Punzara, Loja)")
    
    # 1. Definir CRS del Proyecto estrictamente en EPSG:32717 (WGS 84 / UTM zone 17S)
    crs = QgsCoordinateReferenceSystem("EPSG:32717")
    project.setCrs(crs)
    
    base_dir = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v01-diagnostico-territorial-el-capuli\cartografia_qgis"
    gpkg_path = os.path.join(base_dir, "capuli_punzara_estudio.gpkg")
    output_qgz = os.path.join(base_dir, "proyecto_diagnostico_capuli.qgz")
    output_dxf = os.path.join(base_dir, "capuli_punzara_autocad.dxf")
    
    root = project.layerTreeRoot()
    group_indicadores = root.addGroup("1. Indicadores Territoriales (CPV 2022)")
    group_urbano = root.addGroup("2. Cartografía Urbana (Manzanas y Calles)")
    group_equipamientos = root.addGroup("3. Edificaciones y Predios")
    group_base = root.addGroup("4. Contexto y Satélite")
    
    # --- Capa 1: Sectores Censales (Con Indicadores de Densidad) ---
    print("1. Cargando Sectores Censales...")
    uri_sec = f"{gpkg_path}|layername=sectores_censales_punzara"
    vl_sec = QgsVectorLayer(uri_sec, "Sectores Censales — Punzara (Densidad Pob)", "ogr")
    if vl_sec.isValid():
        ranges = []
        palette = [
            (0, 50, "#fee5d9", "Baja (< 50 hab/km²)"),
            (50, 150, "#fcae91", "Media-Baja (50 - 150 hab/km²)"),
            (150, 300, "#fb6a4a", "Media (150 - 300 hab/km²)"),
            (300, 600, "#de2d26", "Alta (300 - 600 hab/km²)"),
            (600, 99999, "#a50f15", "Muy Alta (> 600 hab/km²)")
        ]
        for lower, upper, color_hex, label in palette:
            sym = QgsSymbol.defaultSymbol(vl_sec.geometryType())
            sym.symbolLayer(0).setColor(QColor(color_hex))
            sym.symbolLayer(0).setStrokeColor(QColor("#2c3e50"))
            sym.symbolLayer(0).setStrokeWidth(0.3)
            sym.setOpacity(0.7) # Semitransparente para ver OpenStreetMap debajo
            ranges.append(QgsRendererRange(lower, upper, sym, label))
            
        renderer = QgsGraduatedSymbolRenderer("densidad_hab_km2", ranges)
        vl_sec.setRenderer(renderer)
        project.addMapLayer(vl_sec, False)
        group_indicadores.addLayer(vl_sec)
        print("   -> Capa de Sectores añadida y estilizada.")
    else:
        print("   Error cargando sectores censales.")

    # --- Capa 2: Manzanas Censales Urbanas ---
    print("2. Cargando Manzanas Urbanas...")
    uri_man = f"{gpkg_path}|layername=manzanas_punzara"
    vl_man = QgsVectorLayer(uri_man, "Manzanas Censales (Punzara / Capulí)", "ogr")
    if vl_man.isValid():
        sym_man = QgsSymbol.defaultSymbol(vl_man.geometryType())
        sym_man.symbolLayer(0).setColor(QColor(0, 0, 0, 0)) # Relleno hueco transparente
        sym_man.symbolLayer(0).setStrokeColor(QColor("#e65100")) # Borde naranja de alta visibilidad
        sym_man.symbolLayer(0).setStrokeWidth(0.6)
        vl_man.setRenderer(QgsSingleSymbolRenderer(sym_man))
        project.addMapLayer(vl_man, False)
        group_urbano.addLayer(vl_man)
        print("   -> Manzanas añadidas.")

    # --- Capa 3: Ejes Viales y Calles ---
    print("3. Cargando Ejes Viales...")
    uri_ejes = f"{gpkg_path}|layername=vias_calles_punzara"
    vl_ejes = QgsVectorLayer(uri_ejes, "Red Vial / Calles", "ogr")
    if vl_ejes.isValid():
        sym_ejes = QgsSymbol.defaultSymbol(vl_ejes.geometryType())
        sym_ejes.symbolLayer(0).setColor(QColor("#37474f")) # Gris oscuro
        sym_ejes.symbolLayer(0).setWidth(0.4)
        vl_ejes.setRenderer(QgsSingleSymbolRenderer(sym_ejes))
        project.addMapLayer(vl_ejes, False)
        group_urbano.addLayer(vl_ejes)
        print("   -> Ejes viales añadidos.")

    # --- Capa 4: Edificaciones ---
    print("4. Cargando Edificaciones Prediales...")
    uri_edif = f"{gpkg_path}|layername=edificaciones_punzara"
    vl_edif = QgsVectorLayer(uri_edif, "Edificaciones / Predios", "ogr")
    if vl_edif.isValid():
        sym_edif = QgsSymbol.defaultSymbol(vl_edif.geometryType())
        sym_edif.symbolLayer(0).setColor(QColor("#1565c0"))
        sym_edif.symbolLayer(0).setSize(1.0)
        sym_edif.symbolLayer(0).setStrokeColor(QColor("#ffffff"))
        sym_edif.symbolLayer(0).setStrokeWidth(0.2)
        vl_edif.setRenderer(QgsSingleSymbolRenderer(sym_edif))
        project.addMapLayer(vl_edif, False)
        node_edif = group_equipamientos.addLayer(vl_edif)
        node_edif.setItemVisibilityChecked(False) # Apagada inicialmente para rapidez
        print("   -> Edificaciones añadidas.")

    # --- Capa 5: OpenStreetMap ---
    print("5. Añadiendo Mapa Base OpenStreetMap...")
    osm_uri = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
    rl_osm = QgsRasterLayer(osm_uri, "OpenStreetMap (Base Vial)", "wms")
    if rl_osm.isValid():
        project.addMapLayer(rl_osm, False)
        group_base.addLayer(rl_osm)
        print("   -> OpenStreetMap añadido.")

    # Configurar extensión de encuadre en el lienzo (Zoom directo a Punzara)
    extent_capuli = QgsRectangle(692500, 9532500, 701500, 9543500)
    ref_rect = QgsReferencedRectangle(extent_capuli, crs)
    project.viewSettings().setDefaultViewExtent(ref_rect)
    
    # Exportar proyecto QGIS
    print(f"Guardando proyecto QGIS en: {output_qgz}")
    project.write(output_qgz)
    print("Proyecto guardado.")

    # Exportar a AutoCAD DXF usando QgsDxfExport
    print(f"Exportando capas vectoriales a DXF para AutoCAD en: {output_dxf}")
    try:
        dxf_export = QgsDxfExport()
        dxf_export.setDestinationCrs(crs)
        layers_to_export = [
            QgsDxfExport.DxfLayer(vl_man),
            QgsDxfExport.DxfLayer(vl_ejes),
            QgsDxfExport.DxfLayer(vl_sec)
        ]
        dxf_export.addLayers(layers_to_export)
        dxf_export.setSymbologyScale(1000)
        
        file_dev = QFile(output_dxf)
        if file_dev.open(QIODevice.WriteOnly):
            res = dxf_export.writeToFile(file_dev, "CP1252")
            file_dev.close()
            print("Archivo DXF para AutoCAD exportado con resultado:", res)
        else:
            print("No se pudo abrir archivo destino DXF.")
    except Exception as e:
        print(f"Aviso exportando DXF: {e}")

    qgs.exitQgis()
    print("Todo completado con éxito.")

if __name__ == "__main__":
    construir_todo()
