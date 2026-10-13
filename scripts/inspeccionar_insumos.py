"""Inspecciona los insumos descargados en lake/raw y el geopackage cartográfico."""

from __future__ import annotations

import sqlite3
import zipfile
from pathlib import Path
import pandas as pd


def inspect_all() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    raw_dir = repo_root / "lake" / "raw"
    gpkg_file = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "cartografia_qgis" / "11_loja.gpkg"

    print("==================================================================")
    print(" 1. ANÁLISIS DE CARTOGRAFÍA (11_loja.gpkg)")
    print("==================================================================")
    if gpkg_file.exists():
        conn = sqlite3.connect(str(gpkg_file))
        cursor = conn.cursor()
        cursor.execute("SELECT table_name, data_type FROM gpkg_contents")
        layers = cursor.fetchall()
        print("Capas vectoriales encontradas:")
        for tbl, dtype in layers:
            cursor.execute(f"SELECT count(*) FROM {tbl}")
            cnt = cursor.fetchone()[0]
            print(f"  • Capa '{tbl}' ({dtype}): {cnt} objetos espaciales")

        print("\nSectores en el Cantón Loja (1101):")
        cursor.execute("SELECT id, parroquia, sec FROM sec_a WHERE parroquia LIKE '1101%' LIMIT 5")
        for r in cursor.fetchall():
            print(f"  Sec ID: {r[0]} | Parroquia: {r[1]} | Sec: {r[2]}")

        print("\nManzanas en el Cantón Loja:")
        cursor.execute("SELECT id, man FROM man_a WHERE id LIKE '1101%' LIMIT 5")
        for r in cursor.fetchall():
            print(f"  Man ID: {r[0]} | Man: {r[1]}")
        conn.close()
    else:
        print("[-] No se encontró 11_loja.gpkg en cartografia_qgis/")

    print("\n==================================================================")
    print(" 2. ANÁLISIS DE DICCIONARIO DE SECTORES (DICCIONARIO_BDD_SECTOR.xlsx)")
    print("==================================================================")
    dicc_file = raw_dir / "DICCIONARIO_BDD_SECTOR.xlsx"
    if dicc_file.exists():
        xl = pd.ExcelFile(dicc_file)
        print("Hojas del diccionario:", xl.sheet_names)
        for s in xl.sheet_names[:4]:
            df_s = xl.parse(s)
            print(f"  • Hoja '{s}': {len(df_s)} variables definidas. Columnas: {list(df_s.columns)}")
            print(f"    Primeras variables: {list(df_s.iloc[:5, 0].values)}")

    print("\n==================================================================")
    print(" 3. ANÁLISIS DE BDD_CPV2022_SECT_CSV.zip")
    print("==================================================================")
    bdd_zip = raw_dir / "BDD_CPV2022_SECT_CSV.zip"
    if bdd_zip.exists():
        with zipfile.ZipFile(bdd_zip, "r") as z:
            for info in z.infolist():
                if info.filename.endswith(".csv"):
                    size_mb = info.file_size / (1024 * 1024)
                    print(f"  • {info.filename}: {size_mb:.2f} MB descomprimido")
                    # Muestra las primeras líneas de una tabla
                    with z.open(info.filename) as f:
                        header = f.readline().decode("utf-8", errors="ignore").strip()
                        print(f"    Variables ({len(header.split(';'))}): {header[:120]}...")

    print("==================================================================")


if __name__ == "__main__":
    inspect_all()
