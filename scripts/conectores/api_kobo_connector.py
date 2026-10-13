"""
Conector a la API v2 de KoboToolbox (kobotoolbox.org)
Permite inspeccionar formularios, descargar encuestas de campo y sincronizar con QGIS/GeoJSON.
"""

import os
import json
import urllib.request
from typing import Dict, Any, List, Optional

class KoboToolboxConnector:
    """Cliente para la API v2 de KoboToolbox (kf.kobotoolbox.org)."""

    BASE_URL = "https://kf.kobotoolbox.org/api/v2"

    def __init__(self, asset_uid: str = "aBJEiLwrvSWwb7fBrukk8a", api_token: Optional[str] = None):
        self.asset_uid = asset_uid
        self.api_token = api_token

    def _get_headers(self) -> Dict[str, str]:
        headers = {"User-Agent": "UNL-Practicas-Arquitectura/1.0"}
        if self.api_token:
            headers["Authorization"] = f"Token {self.api_token}"
        return headers

    def obtener_formulario(self) -> Dict[str, Any]:
        """Obtiene la metadata y esquema de preguntas del formulario."""
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/"
        req = urllib.request.Request(url, headers=self._get_headers())
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def obtener_respuestas_campo(self) -> List[Dict[str, Any]]:
        """Descarga las respuestas y encuestas enviadas desde territorio."""
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/data.json"
        req = urllib.request.Request(url, headers=self._get_headers())
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("results", [])

    def exportar_a_geojson(self, respuestas: List[Dict[str, Any]], destino_geojson: str) -> bool:
        """Convierte los puntos GPS de las encuestas en una capa espacial GeoJSON para QGIS."""
        features = []
        for r in respuestas:
            # Buscar coordenadas GPS registradas (campo _geolocation o similar)
            geo = r.get("_geolocation")
            if geo and len(geo) >= 2 and geo[0] is not None and geo[1] is not None:
                lat, lon = geo[0], geo[1]
                feat = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(lon), float(lat)]
                    },
                    "properties": {k: v for k, v in r.items() if not k.startswith("_")}
                }
                features.append(feat)
                
        geojson_data = {
            "type": "FeatureCollection",
            "name": "encuestas_campo_capuli",
            "features": features
        }
        with open(destino_geojson, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=2)
        print(f"Capa espacial de encuestas guardada con {len(features)} puntos en: {destino_geojson}")
        return True

if __name__ == "__main__":
    kobo = KoboToolboxConnector()
    print("Conectando con KoboToolbox...")
    form = kobo.obtener_formulario()
    print(f"Formulario: {form.get('name')}")
    print(f"Propietario: {form.get('owner__username')}")
    print(f"Estado Despliegue: {'ACTIVO' if form.get('deployment__active') else 'INACTIVO'}")
    print(f"Total respuestas registradas: {form.get('deployment__submission_count')}")
