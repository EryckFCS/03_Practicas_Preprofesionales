"""Extrae y filtra los microdatos censales de Loja (1101) desde el ZIP oficial."""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path


def process_loja_census() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    zip_path = repo_root / "lake" / "raw" / "BDD_CPV2022_SECT_CSV.zip"
    out_dir = repo_root / "docs" / "vaults" / "v01-diagnostico-territorial-el-capuli" / "datos_redatam"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not zip_path.exists():
        print(f"[-] No se encontró {zip_path}")
        return

    targets = [
        ("1.2 BDD_CPV_2022_SECTOR_CSV/CPV_2022_Vivienda_Sector.csv", "cpv2022_loja_vivienda_sector.csv"),
        ("1.2 BDD_CPV_2022_SECTOR_CSV/CPV_2022_Hogar_Sector.csv", "cpv2022_loja_hogar_sector.csv"),
        ("1.2 BDD_CPV_2022_SECTOR_CSV/CPV_2022_Poblacion_Sector.csv", "cpv2022_loja_poblacion_sector.csv"),
    ]

    print("==================================================================")
    print(" EXTRACCIÓN DE DATOS CENSALES 2022: CANTÓN LOJA (1101)")
    print("==================================================================")

    with zipfile.ZipFile(zip_path, "r") as z:
        for archive_name, out_name in targets:
            out_file = out_dir / out_name
            print(f"[*] Procesando {out_name} desde {archive_name}...")
            
            with z.open(archive_name) as infile, open(out_file, "w", encoding="utf-8", newline="") as outfile:
                reader = csv.reader((line.decode("utf-8", errors="ignore") for line in infile), delimiter=";")
                writer = csv.writer(outfile)
                
                header = next(reader)
                writer.writerow(header)
                
                i01_idx = header.index("I01")
                i02_idx = header.index("I02")
                
                match_count = 0
                for row in reader:
                    if len(row) > i02_idx and row[i01_idx] == "11" and row[i02_idx] == "01":
                        writer.writerow(row)
                        match_count += 1
                        
            size_mb = out_file.stat().st_size / (1024 * 1024)
            print(f"  [+] Generado {out_name}: {match_count:,} registros ({size_mb:.2f} MB)")

    print("==================================================================")
    print(" Extracción finalizada exitosamente.")
    print(f" Archivos depositados en: {out_dir}")
    print("==================================================================")


if __name__ == "__main__":
    process_loja_census()
