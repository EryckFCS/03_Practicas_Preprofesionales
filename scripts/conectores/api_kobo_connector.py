"""
Conector Soberano a la API v2 de KoboToolbox (kobotoolbox.org)
Permite inspeccionar, editar preguntas, redesplegar formularios y sincronizar respuestas de campo.
Carga automáticamente las credenciales desde el archivo local .env (ignorado en Git).
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

def _cargar_env() -> Dict[str, str]:
    """Carga variables del archivo .env local si existe."""
    env_vars = {}
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
    return env_vars

class KoboToolboxConnector:
    """Cliente para la API v2 de KoboToolbox (kf.kobotoolbox.org)."""

    BASE_URL = "https://kf.kobotoolbox.org/api/v2"

    def __init__(self, asset_uid: Optional[str] = None, api_token: Optional[str] = None):
        env = _cargar_env()
        self.asset_uid = asset_uid or env.get("KOBO_FORM_UID", "aBJEiLwrvSWwb7fBrukk8a")
        self.api_token = api_token or env.get("KOBO_API_TOKEN")

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": "UNL-Practicas-Arquitectura/1.0",
            "Content-Type": "application/json"
        }
        if self.api_token:
            headers["Authorization"] = f"Token {self.api_token}"
        return headers

    def obtener_formulario(self) -> Dict[str, Any]:
        """Obtiene la metadata completa, esquema y preguntas del formulario."""
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/"
        req = urllib.request.Request(url, headers=self._get_headers())
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def actualizar_contenido_formulario(self, nuevo_content: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza el esquema de preguntas del formulario mediante PATCH."""
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/"
        payload = json.dumps({"content": nuevo_content}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=self._get_headers(), method="PATCH")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def redesplegar_formulario(self, version_id: Optional[str] = None) -> Dict[str, Any]:
        """Vuelve a desplegar el formulario (Redeploy) para que los cambios se activen en los celulares."""
        if not version_id:
            form = self.obtener_formulario()
            version_id = form.get("version_id")
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/deployment/"
        payload = json.dumps({"active": True, "version_id": version_id}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=self._get_headers(), method="PATCH")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def obtener_respuestas_campo(self) -> List[Dict[str, Any]]:
        """Descarga las encuestas levantadas en territorio (data submissions)."""
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/data.json"
        req = urllib.request.Request(url, headers=self._get_headers())
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("results", [])

    def editar_respuesta(self, submission_id: str, nuevos_datos: Dict[str, Any]) -> Dict[str, Any]:
        """Permite editar y corregir una encuesta ya enviada desde territorio."""
        url = f"{self.BASE_URL}/assets/{self.asset_uid}/data/{submission_id}/"
        payload = json.dumps(nuevos_datos).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=self._get_headers(), method="PATCH")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def exportar_a_geojson(self, respuestas: List[Dict[str, Any]], destino_geojson: str) -> bool:
        """Convierte los puntos de encuesta en una capa GeoJSON para QGIS."""
        features = []
        for r in respuestas:
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
    print("Probando conector soberano con token...")
    form = kobo.obtener_formulario()
    print(f"Formulario: {form.get('name')}")
    print(f"Usuario autenticado: {form.get('owner__username')}")
    print(f"Permisos efectivos: {form.get('effective_permissions')}")
