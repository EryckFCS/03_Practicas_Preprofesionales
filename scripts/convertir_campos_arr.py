import os
import json
import pandas as pd

def procesar_campos_arr():
    raw_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\lake\raw\CAMPOS ARR.xls"
    proc_dir = r"d:\08_Ciclo\03_Practicas_Preprofesionales\lake\processed"
    os.makedirs(proc_dir, exist_ok=True)
    
    json_out = os.path.join(proc_dir, "campos_arr.json")
    md_out = os.path.join(proc_dir, "campos_arr.md")
    
    df = pd.read_excel(raw_path, sheet_name="Hoja1", header=None)
    print(f"Filas leidas: {len(df)}, Columnas: {df.shape[1]}")
    
    items = []
    seccion_actual = "GENERAL"
    
    for idx, row in df.iterrows():
        val = row.iloc[0]
        if pd.isna(val):
            continue
        val_str = str(val).strip()
        if not val_str:
            continue
            
        items.append({
            "fila": int(idx) + 1,
            "texto": val_str
        })
        
    print(f"Total campos no vacios extraidos: {len(items)}")
    
    # Guardar en JSON ligero
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Guardado en JSON: {json_out} ({os.path.getsize(json_out)} bytes)")
    
    # Guardar en Markdown limpio
    with open(md_out, "w", encoding="utf-8") as f:
        f.write("# Campos A.R.R. (Aproximación Rápida Rural / Comunitaria)\n\n")
        f.write(f"Total de campos identificados: {len(items)}\n\n")
        f.write("| Nro | Código / Campo |\n")
        f.write("| :---: | :--- |\n")
        for i, item in enumerate(items, 1):
            f.write(f"| {i} | {item['texto']} |\n")
    print(f"Guardado en Markdown: {md_out} ({os.path.getsize(md_out)} bytes)")

if __name__ == "__main__":
    procesar_campos_arr()
