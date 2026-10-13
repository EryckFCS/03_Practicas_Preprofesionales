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

def construir_proyecto_qgis():
    print("=" * 70)
    print("CONSTRUYENDO PROYECTO QGIS DEFINITIVO: INEC + CATASTRO MUNICIPAL")
    print("=" * 70)
    
    qgs = QgsApplication([], False)
    qgs.initQgis()
    
    project = QgsProject.instance()
    project.clear()
    project.setTitle("Diagnóstico Territorial y Catastral — Barrio El Capulí (Loja)")
    
    # CRS Obligatorio Oficial: EPSG:32717 (WGS 84 / UTM zone 17S)
    crs = QgsCoordinateReferenceSystem("EPSG:32717")
    project.setCrs(crs)
    
    base_dir = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v01-diagnostico-territorial-el-capuli\cartografia_qgis"
    gpkg_path = os.path.join(base_dir, "capuli_punzara_estudio.gpkg")
    output_qgz = os.path.join(base_dir, "proyecto_diagnostico_capuli.qgz")
    output_dxf = os.path.join(base_dir, "capuli_punzara_autocad.dxf")
    
    root = project.layerTreeRoot()
    group_estudio = root.addGroup("1. Área de Estudio y Demografía (INEC CPV 2022)")
    group_catastro = root.addGroup("2. Catastro Municipal de Loja (Predios y Construcciones)")
    group_vial = root.addGroup("3. Vialidad e Infraestructura (Calles y Bombeo)")
    group_base = root.addGroup("4. Mapa Base y Contexto Territorial")
    
    # -------------------------------------------------------------
    # 1. Capa: Sectores de Estudio de El Capulí (10 Sectores clave)
    # -------------------------------------------------------------
    print("1. Cargando 10 Sectores Censales de El Capulí...")
    uri_sec = f"{gpkg_path}|layername=sectores_estudio_capuli_10"
    vl_sec = QgsVectorLayer(uri_sec, "10 Sectores Censales — El Capulí (INEC)", "ogr")
    if vl_sec.isValid():
        sym_sec = QgsSymbol.defaultSymbol(vl_sec.geometryType())
        sym_sec.symbolLayer(0).setColor(QColor(230, 81, 0, 40)) # Naranja translúcido
        sym_sec.symbolLayer(0).setStrokeColor(QColor("#d84315"))
        sym_sec.symbolLayer(0).setStrokeWidth(0.8)
        vl_sec.setRenderer(QgsSingleSymbolRenderer(sym_sec))
        project.addMapLayer(vl_sec, False)
        group_estudio.addLayer(vl_sec)
        print("   -> Capa de 10 sectores añadida.")
    
    # -------------------------------------------------------------
    # 2. Capa: Manzanas Censales del Área de Estudio
    # -------------------------------------------------------------
    print("2. Cargando Manzanas Censales...")
    uri_man = f"{gpkg_path}|layername=manzanas_estudio_capuli"
    vl_man = QgsVectorLayer(uri_man, "Manzanas Censales (INEC 2022)", "ogr")
    if vl_man.isValid():
        sym_man = QgsSymbol.defaultSymbol(vl_man.geometryType())
        sym_man.symbolLayer(0).setColor(QColor(0, 0, 0, 0)) # Relleno transparente
        sym_man.symbolLayer(0).setStrokeColor(QColor("#e65100"))
        sym_man.symbolLayer(0).setStrokeWidth(0.5)
        vl_man.setRenderer(QgsSingleSymbolRenderer(sym_man))
        project.addMapLayer(vl_man, False)
        group_estudio.addLayer(vl_man)
        print("   -> Manzanas añadidas.")

    # -------------------------------------------------------------
    # 3. Capa: Edificaciones Censales (INEC)
    # -------------------------------------------------------------
    print("3. Cargando Edificaciones Censales...")
    uri_edif = f"{gpkg_path}|layername=edificaciones_estudio_capuli"
    vl_edif = QgsVectorLayer(uri_edif, "Edificaciones Censales (INEC)", "ogr")
    if vl_edif.isValid():
        sym_edif = QgsSymbol.defaultSymbol(vl_edif.geometryType())
        sym_edif.symbolLayer(0).setColor(QColor("#3949ab"))
        sym_edif.symbolLayer(0).setSize(1.2)
        sym_edif.symbolLayer(0).setStrokeColor(QColor("#ffffff"))
        sym_edif.symbolLayer(0).setStrokeWidth(0.2)
        vl_edif.setRenderer(QgsSingleSymbolRenderer(sym_edif))
        project.addMapLayer(vl_edif, False)
        node_ed = group_estudio.addLayer(vl_edif)
        node_ed.setItemVisibilityChecked(False)
        print("   -> Edificaciones censales añadidas.")

    # -------------------------------------------------------------
    # 4. Capa Municipal: Predios Urbanos
    # -------------------------------------------------------------
    print("4. Cargando Predios Urbanos del Municipio...")
    uri_pu = f"{gpkg_path}|layername=muni_predios_urbanos_capuli"
    vl_pu = QgsVectorLayer(uri_pu, "Predios Urbanos (Catastro Municipal)", "ogr")
    if vl_pu.isValid():
        sym_pu = QgsSymbol.defaultSymbol(vl_pu.geometryType())
        sym_pu.symbolLayer(0).setColor(QColor(76, 175, 80, 50)) # Verde translúcido
        sym_pu.symbolLayer(0).setStrokeColor(QColor("#2e7d32"))
        sym_pu.symbolLayer(0).setStrokeWidth(0.4)
        vl_pu.setRenderer(QgsSingleSymbolRenderer(sym_pu))
        project.addMapLayer(vl_pu, False)
        group_catastro.addLayer(vl_pu)
        print("   -> Predios urbanos añadidos.")

    # -------------------------------------------------------------
    # 5. Capa Municipal: Predios Rurales
    # -------------------------------------------------------------
    print("5. Cargando Predios Rurales del Municipio...")
    uri_pr = f"{gpkg_path}|layername=muni_predios_rurales_capuli"
    vl_pr = QgsVectorLayer(uri_pr, "Predios Rurales (Catastro Municipal)", "ogr")
    if vl_pr.isValid():
        sym_pr = QgsSymbol.defaultSymbol(vl_pr.geometryType())
        sym_pr.symbolLayer(0).setColor(QColor(158, 157, 36, 40)) # Amarillo verdoso translúcido
        sym_pr.symbolLayer(0).setStrokeColor(QColor("#827717"))
        sym_pr.symbolLayer(0).setStrokeWidth(0.4)
        vl_pr.setRenderer(QgsSingleSymbolRenderer(sym_pr))
        project.addMapLayer(vl_pr, False)
        group_catastro.addLayer(vl_pr)
        print("   -> Predios rurales añadidos.")

    # -------------------------------------------------------------
    # 6. Capa Municipal: Construcciones Rurales (Bloques/Huellas)
    # -------------------------------------------------------------
    print("6. Cargando Construcciones Rurales del Municipio...")
    uri_cr = f"{gpkg_path}|layername=muni_construcciones_rurales_capuli"
    vl_cr = QgsVectorLayer(uri_cr, "Construcciones y Bloques (Municipio)", "ogr")
    if vl_cr.isValid():
        sym_cr = QgsSymbol.defaultSymbol(vl_cr.geometryType())
        sym_cr.symbolLayer(0).setColor(QColor("#d32f2f")) # Rojo teja
        sym_cr.symbolLayer(0).setStrokeColor(QColor("#b71c1c"))
        sym_cr.symbolLayer(0).setStrokeWidth(0.3)
        vl_cr.setRenderer(QgsSingleSymbolRenderer(sym_cr))
        project.addMapLayer(vl_cr, False)
        group_catastro.addLayer(vl_cr)
        print("   -> Construcciones rurales añadidas.")

    # -------------------------------------------------------------
    # 7. Capa Municipal: Vialidad Oficial Municipal
    # -------------------------------------------------------------
    print("7. Cargando Red Vial Municipal...")
    uri_v = f"{gpkg_path}|layername=muni_vialidad_capuli"
    vl_v = QgsVectorLayer(uri_v, "Red Vial Municipal (Jerarquía y Rodadura)", "ogr")
    if vl_v.isValid():
        sym_v = QgsSymbol.defaultSymbol(vl_v.geometryType())
        sym_v.symbolLayer(0).setColor(QColor("#212121"))
        sym_v.symbolLayer(0).setWidth(0.6)
        vl_v.setRenderer(QgsSingleSymbolRenderer(sym_v))
        project.addMapLayer(vl_v, False)
        group_vial.addLayer(vl_v)
        print("   -> Red vial municipal añadida.")

    # -------------------------------------------------------------
    # 8. Capa Municipal: Estaciones de Bombeo
    # -------------------------------------------------------------
    print("8. Cargando Estaciones de Bombeo...")
    uri_eb = f"{gpkg_path}|layername=muni_estaciones_bombeo_loja"
    vl_eb = QgsVectorLayer(uri_eb, "Estaciones de Bombeo de Agua", "ogr")
    if vl_eb.isValid():
        sym_eb = QgsSymbol.defaultSymbol(vl_eb.geometryType())
        sym_eb.symbolLayer(0).setColor(QColor("#0288d1"))
        sym_eb.symbolLayer(0).setStrokeColor(QColor("#01579b"))
        sym_eb.symbolLayer(0).setStrokeWidth(0.5)
        vl_eb.setRenderer(QgsSingleSymbolRenderer(sym_eb))
        project.addMapLayer(vl_eb, False)
        node_eb = group_vial.addLayer(vl_eb)
        node_eb.setItemVisibilityChecked(False)
        print("   -> Estaciones de bombeo añadidas.")

    # -------------------------------------------------------------
    # 9. Mapa Base OpenStreetMap
    # -------------------------------------------------------------
    print("9. Añadiendo Mapa Base OpenStreetMap...")
    osm_uri = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
    rl_osm = QgsRasterLayer(osm_uri, "OpenStreetMap (Base Vial y Satelital)", "wms")
    if rl_osm.isValid():
        project.addMapLayer(rl_osm, False)
        group_base.addLayer(rl_osm)
        print("   -> OpenStreetMap añadido.")

    # -------------------------------------------------------------
    # 10. Encuadre directo a El Capulí (Campus San Gerardo / Av. Yangana)
    # -------------------------------------------------------------
    # Centro en X: 700420, Y: 9551855 con ventana de 3.5 km x 3.5 km
    extent_capuli = QgsRectangle(698500, 9550000, 702500, 9553800)
    ref_rect = QgsReferencedRectangle(extent_capuli, crs)
    project.viewSettings().setDefaultViewExtent(ref_rect)
    
    # Guardar proyecto QGIS
    print(f"\nGuardando archivo de proyecto QGIS en: {output_qgz}")
    project.write(output_qgz)
    print("   -> ¡Proyecto QGIS actualizado y guardado!")

    # -------------------------------------------------------------
    # 11. Exportar a AutoCAD DXF (Capas prediales y viales de El Capulí)
    # -------------------------------------------------------------
    print(f"\nExportando a AutoCAD DXF en: {output_dxf}...")
    try:
        dxf_export = QgsDxfExport()
        dxf_export.setDestinationCrs(crs)
        layers_to_export = []
        if vl_man.isValid():
            layers_to_export.append(QgsDxfExport.DxfLayer(vl_man))
        if vl_v.isValid():
            layers_to_export.append(QgsDxfExport.DxfLayer(vl_v))
        if vl_sec.isValid():
            layers_to_export.append(QgsDxfExport.DxfLayer(vl_sec))
        if vl_cr.isValid():
            layers_to_export.append(QgsDxfExport.DxfLayer(vl_cr))
            
        dxf_export.addLayers(layers_to_export)
        dxf_export.setSymbologyScale(1000)
        
        file_dev = QFile(output_dxf)
        if file_dev.open(QIODevice.WriteOnly):
            res = dxf_export.writeToFile(file_dev, "CP1252")
            file_dev.close()
            print("   -> Archivo DXF para AutoCAD generado con éxito.")
        else:
            print("   -> No se pudo abrir archivo destino DXF.")
    except Exception as e:
        print(f"   Aviso exportando DXF: {e}")

    qgs.exitQgis()
    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO EXITOSAMENTE.")
    print("=" * 70)

if __name__ == "__main__":
    construir_proyecto_qgis()
