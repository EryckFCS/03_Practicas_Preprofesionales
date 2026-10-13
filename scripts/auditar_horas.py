"""Script de auditoría de horas acumuladas para Prácticas Preprofesionales."""

from __future__ import annotations

import json
import re
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config_file = repo_root / "config" / "node_config.json"
    bitacoras_dir = repo_root / "informes" / "01_bitacoras_semanales"

    target_hours = 240
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                target_hours = data.get("hours_management", {}).get("target_hours", 240)
        except Exception as e:
            print(f"[!] Error leyendo config: {e}")

    print("==================================================================")
    print(" AUDITORÍA DE HORAS: PRÁCTICAS PREPROFESIONALES (ARQUITECTURA) ")
    print("==================================================================")
    print(f"Meta reglamentaria: {target_hours} horas\n")

    total_accumulated = 0.0
    bitacora_files = sorted(bitacoras_dir.glob("*.md"))

    if not bitacora_files or all(f.name == "README.md" for f in bitacora_files):
        print("[-] No se han registrado bitácoras de actividades todavía.")
        print(f"[-] Ubicación esperada: {bitacoras_dir}")
        print("------------------------------------------------------------------")
        print(f"Progreso actual: 0.0 / {target_hours} horas (0.00%)")
        print("==================================================================")
        return

    hour_pattern = re.compile(
        r"(?:horas?|total_horas|horas_dedicadas)\s*[:|=]\s*(\d+(?:\.\d+)?)",
        re.IGNORECASE,
    )
    table_pattern = re.compile(
        r"\|\s*Total\s*(?:Horas)?\s*\|\s*(\d+(?:\.\d+)?)\s*\|",
        re.IGNORECASE,
    )

    for b in bitacora_files:
        if b.name == "README.md":
            continue
        try:
            text = b.read_text(encoding="utf-8")
            hours_found = 0.0
            t_match = table_pattern.search(text)
            if t_match:
                hours_found = float(t_match.group(1))
            else:
                h_matches = hour_pattern.findall(text)
                if h_matches:
                    hours_found = sum(float(x) for x in h_matches)
            total_accumulated += hours_found
            print(f"  • {b.name}: {hours_found:.1f} horas")
        except Exception as err:
            print(f"  [!] Error leyendo {b.name}: {err}")

    percentage = (total_accumulated / target_hours) * 100 if target_hours > 0 else 0
    remaining = max(0.0, target_hours - total_accumulated)

    print("------------------------------------------------------------------")
    print(f"Total acumulado : {total_accumulated:.1f} horas")
    print(f"Horas restantes : {remaining:.1f} horas")
    print(f"Porcentaje      : {percentage:.2f}% completado")
    print("==================================================================")


if __name__ == "__main__":
    main()
