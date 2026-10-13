"""
Conector al Motor y API de RedatamX (CEPAL / CELADE)
Permite interactuar con RedatamX por CLI (rxapp.exe) y por microservicio REST (rxrest.exe).
"""

import os
import subprocess
import json
import urllib.request
from typing import Dict, Any, Optional

class RedatamXConnector:
    """Conector soberano al motor RedatamX instalado en Windows."""

    def __init__(self, redatam_dir: str = r"C:\Program Files\RedatamX"):
        self.redatam_dir = redatam_dir
        self.rxapp_exe = os.path.join(redatam_dir, "rxapp.exe")
        self.rxrest_exe = os.path.join(redatam_dir, "rxrest.exe")
        self.redx_process_exe = os.path.join(redatam_dir, "RedX Process.exe")

    def verificar_instalacion(self) -> Dict[str, Any]:
        """Comprueba el estado de los binarios instalados de RedatamX."""
        return {
            "directorio": self.redatam_dir,
            "existe_directorio": os.path.exists(self.redatam_dir),
            "rxapp_cli": os.path.exists(self.rxapp_exe),
            "rxrest_api": os.path.exists(self.rxrest_exe),
            "redx_gui": os.path.exists(self.redx_process_exe)
        }

    def obtener_info_motor(self) -> str:
        """Consulta la versión y estado del motor RedEngine mediante CLI."""
        if not os.path.exists(self.rxapp_exe):
            return "RedatamX no se encuentra instalado en la ruta esperada."
        try:
            res = subprocess.run([self.rxapp_exe, "--info"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception as e:
            return f"Error ejecutando rxapp: {e}"

    def abrir_diccionario_gui(self, ruta_dicx: str) -> bool:
        """Abre un archivo de diccionario oficial (.dicx) directamente en la interfaz RedX Process."""
        if not os.path.exists(self.redx_process_exe):
            print(f"[Error] No se encuentra {self.redx_process_exe}")
            return False
        try:
            subprocess.Popen([self.redx_process_exe, ruta_dicx])
            print(f"Abriendo RedX Process con diccionario: {ruta_dicx}")
            return True
        except Exception as e:
            print(f"Error abriendo RedX: {e}")
            return False

    def generar_script_spc(self, dicx_path: str, seleccion_parroquia: str = "110156", output_spc: str = "consulta.spc") -> str:
        """Genera un archivo de sintaxis .spc para consulta desatendida en Redatam."""
        script_content = f"""// Script generado para Censo 2022 Punzara / El Capuli
RUNDIC "{dicx_path}"
SELECTION INLINE
    PARROQUIA = "{seleccion_parroquia}"
TABLE t1 AS CROSSTABS
    OF PERSONA.P01 BY PERSONA.P03
    TITLE "Poblacion por Sexo y Grupos de Edad - Punzara"
"""
        with open(output_spc, "w", encoding="utf-8") as f:
            f.write(script_content)
        return output_spc

if __name__ == "__main__":
    con = RedatamXConnector()
    print("Verificando instalación de RedatamX...")
    info = con.verificar_instalacion()
    print(json.dumps(info, indent=2))
    if info["rxapp_cli"]:
        print("\nInformación del Motor RedEngine:")
        print(con.obtener_info_motor()[:300])
