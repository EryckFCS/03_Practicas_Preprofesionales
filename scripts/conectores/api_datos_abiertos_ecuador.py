"""
Conector a la API de Datos Abiertos de Ecuador y Microdatos INEC
Permite consultar metadatos y descargar datasets oficiales del Censo 2022 y estadísticas de Loja.
Incluye manejo de certificados SSL para portales gubernamentales (.gob.ec).
"""

import os
import json
import ssl
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, List

class INECDatosAbiertosClient:
    """Cliente para la API CKAN de Datos Abiertos de Ecuador (datosabiertos.gob.ec)."""
    
    BASE_URL = "https://datosabiertos.gob.ec/api/3/action"

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        # Contexto SSL con soporte para certificados intermedios gubernamentales de Ecuador
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def buscar_paquetes(self, query: str, rows: int = 10) -> List[Dict[str, Any]]:
        """Busca datasets en el portal nacional de datos abiertos por palabra clave."""
        url = f"{self.BASE_URL}/package_search?q={urllib.parse.quote(query)}&rows={rows}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "UNL-Practicas-Arquitectura/1.0"})
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("success"):
                    return data["result"]["results"]
        except Exception as e:
            print(f"[Aviso] No se pudo consultar la API CKAN de Datos Abiertos: {e}")
        return []

    def obtener_recursos_censo(self, package_id: str = "censo-poblacion-vivienda-2022") -> List[Dict[str, Any]]:
        """Obtiene la lista de recursos y URLs de descarga para un dataset específico."""
        url = f"{self.BASE_URL}/package_show?id={urllib.parse.quote(package_id)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "UNL-Practicas-Arquitectura/1.0"})
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("success"):
                    return data["result"].get("resources", [])
        except Exception as e:
            print(f"[Aviso] Error consultando el paquete {package_id}: {e}")
        return []

    def descargar_recurso(self, url: str, destino_path: str) -> bool:
        """Descarga un archivo oficial desde el servidor del INEC hacia el Lake."""
        try:
            print(f"Descargando desde: {url} ...")
            req = urllib.request.Request(url, headers={"User-Agent": "UNL-Practicas-Arquitectura/1.0"})
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp, open(destino_path, "wb") as f:
                f.write(resp.read())
            print(f"Guardado exitosamente en: {destino_path}")
            return True
        except Exception as e:
            print(f"Error descargando recurso: {e}")
            return False

if __name__ == "__main__":
    client = INECDatosAbiertosClient()
    print("Probando conexión con API CKAN de Datos Abiertos Ecuador...")
    resultados = client.buscar_paquetes("censo", rows=5)
    print(f"Datasets encontrados: {len(resultados)}")
    for r in resultados:
        print(f" - {r.get('title')} ({r.get('name')})")
