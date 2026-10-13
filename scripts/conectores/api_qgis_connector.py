"""
Conector al Motor y API de QGIS (OSGeo4W / PyQGIS / qgis_process)
Permite ejecutar geoprocesos de análisis territorial y generación de proyectos de forma desatendida.
"""

import os
import subprocess
import json
from typing import Dict, Any, List, Optional

class QGISHeadlessConnector:
    """Conector soberano al motor QGIS instalado mediante OSGeo4W."""

    def __init__(self, osgeo4w_dir: str = r"C:\Users\ERICK-FCS\AppData\Local\Programs\OSGeo4W"):
        self.osgeo4w_dir = osgeo4w_dir
        self.bin_dir = os.path.join(osgeo4w_dir, "bin")
        self.qgis_process_bat = os.path.join(self.bin_dir, "qgis_process-qgis-ltr.bat")
        self.python_qgis_bat = os.path.join(self.bin_dir, "python-qgis-ltr.bat")

    def verificar_instalacion(self) -> Dict[str, Any]:
        """Comprueba el estado de las herramientas de consola de QGIS."""
        return {
            "osgeo4w_dir": self.osgeo4w_dir,
            "existe_osgeo4w": os.path.exists(self.osgeo4w_dir),
            "qgis_process_cli": os.path.exists(self.qgis_process_bat),
            "python_qgis_env": os.path.exists(self.python_qgis_bat)
        }

    def obtener_version(self) -> str:
        """Obtiene la versión oficial de QGIS LTR instalada."""
        if not os.path.exists(self.qgis_process_bat):
            return "qgis_process no encontrado."
        try:
            res = subprocess.run([self.qgis_process_bat, "--version"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception as e:
            return f"Error ejecutando QGIS: {e}"

    def ejecutar_script_pyqgis(self, script_path: str, args: Optional[List[str]] = None) -> subprocess.CompletedProcess:
        """Ejecuta un script de Python dentro del entorno completo de PyQGIS (con GDAL, PROJ, GEOS)."""
        if not os.path.exists(self.python_qgis_bat):
            raise FileNotFoundError(f"No se encontró {self.python_qgis_bat}")
        cmd = [self.python_qgis_bat, script_path] + (args or [])
        return subprocess.run(cmd, capture_output=True, text=True)

    def ejecutar_algoritmo(self, alg_name: str, params: Dict[str, Any]) -> subprocess.CompletedProcess:
        """Ejecuta un algoritmo nativo de QGIS mediante la consola qgis_process."""
        cmd = [self.qgis_process_bat, "run", alg_name, "--"]
        for k, v in params.items():
            cmd.append(f"{k}={v}")
        return subprocess.run(cmd, capture_output=True, text=True)

if __name__ == "__main__":
    qgis = QGISHeadlessConnector()
    print("Verificando instalación de QGIS LTR...")
    info = qgis.verificar_instalacion()
    print(json.dumps(info, indent=2))
    if info["qgis_process_cli"]:
        print("\nVersión de QGIS:")
        print(qgis.obtener_version()[:250])
