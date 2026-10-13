"""
Módulo de Conectores y APIs para Prácticas Preprofesionales de Arquitectura (UNL).
Integra:
1. INECDatosAbiertosClient (CKAN Datos Abiertos Ecuador)
2. RedatamXConnector (RedatamX CLI / REST)
3. QGISHeadlessConnector (OSGeo4W / PyQGIS / qgis_process)
"""

from .api_datos_abiertos_ecuador import INECDatosAbiertosClient
from .api_redatam_connector import RedatamXConnector
from .api_qgis_connector import QGISHeadlessConnector

__all__ = [
    "INECDatosAbiertosClient",
    "RedatamXConnector",
    "QGISHeadlessConnector"
]
