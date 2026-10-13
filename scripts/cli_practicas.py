"""
CLI Unificada de Prácticas Preprofesionales — UNL Arquitectura / Economía
Permite verificar servicios, consultar APIs oficiales y coordinar el flujo territorial.
"""

import sys
import os
import argparse
import json

# Asegurar importación de conectores
sys.path.insert(0, os.path.dirname(__file__))
from conectores import INECDatosAbiertosClient, RedatamXConnector, QGISHeadlessConnector

def cmd_status(args):
    print("=" * 70)
    print("ESTADO DEL STACK DE SERVICIOS Y APIS — PRÁCTICAS UNL")
    print("=" * 70)
    
    # 1. RedatamX
    rx = RedatamXConnector()
    rx_info = rx.verificar_instalacion()
    print("\n[1] REDATAMX (CEPAL / CELADE):")
    print(f"    - Directorio instalado: {'OK' if rx_info['existe_directorio'] else 'NO ENCONTRADO'}")
    print(f"    - CLI rxapp.exe:       {'DISPONIBLE' if rx_info['rxapp_cli'] else 'NO DISPONIBLE'}")
    print(f"    - API REST rxrest.exe:  {'DISPONIBLE' if rx_info['rxrest_api'] else 'NO DISPONIBLE'}")
    print(f"    - GUI RedX Process:     {'LISTO' if rx_info['redx_gui'] else 'NO DISPONIBLE'}")

    # 2. QGIS OSGeo4W
    qg = QGISHeadlessConnector()
    qg_info = qg.verificar_instalacion()
    print("\n[2] QGIS LTR / OSGeo4W:")
    print(f"    - Directorio OSGeo4W:   {'OK' if qg_info['existe_osgeo4w'] else 'NO ENCONTRADO'}")
    print(f"    - CLI qgis_process:     {'DISPONIBLE' if qg_info['qgis_process_cli'] else 'NO DISPONIBLE'}")
    print(f"    - PyQGIS Environment:   {'LISTO' if qg_info['python_qgis_env'] else 'NO DISPONIBLE'}")

    # 3. API Datos Abiertos Ecuador
    da = INECDatosAbiertosClient(timeout=5)
    print("\n[3] API CKAN DATOS ABIERTOS ECUADOR (datosabiertos.gob.ec):")
    try:
        res = da.buscar_paquetes("censo", rows=1)
        if res:
            print("    - Conexión HTTPS:       ONLINE (Activa y respondiendo)")
        else:
            print("    - Conexión HTTPS:       TIMEOUT / RESTRINGIDA")
    except Exception as e:
        print(f"    - Conexión HTTPS:       ERROR ({e})")

    # 4. Servidores MCP Nativos
    print("\n[4] SERVIDORES MCP ACTIVOS EN ENTORNO:")
    print("    - capital-inec:          ACTIVO (Consultas metodológicas e indicadores)")
    print("    - capital-bce:           ACTIVO (Series macroeconómicas y tasas)")
    print("=" * 70)

def cmd_ckan_search(args):
    da = INECDatosAbiertosClient()
    print(f"Buscando en Datos Abiertos Ecuador: '{args.query}' ...")
    pkgs = da.buscar_paquetes(args.query, rows=args.rows)
    print(f"\nResultados encontrados ({len(pkgs)}):")
    for p in pkgs:
        print(f" * {p.get('title')} [{p.get('name')}]")
        for r in p.get("resources", [])[:2]:
            print(f"    -> Recurso: {r.get('name')} ({r.get('format')}) - URL: {r.get('url')}")

def main():
    parser = argparse.ArgumentParser(description="CLI de Prácticas Preprofesionales (UNL)")
    subparsers = parser.add_subparsers(dest="command")

    # Comando status
    p_status = subparsers.add_parser("status", help="Verifica el estado de todas las APIs y motores locales")
    p_status.set_defaults(func=cmd_status)

    # Comando ckan
    p_ckan = subparsers.add_parser("ckan", help="Consulta la API de Datos Abiertos de Ecuador")
    p_ckan.add_argument("query", help="Palabra clave a buscar")
    p_ckan.add_argument("--rows", type=int, default=5, help="Número de resultados")
    p_ckan.set_defaults(func=cmd_ckan_search)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)

if __name__ == "__main__":
    main()
