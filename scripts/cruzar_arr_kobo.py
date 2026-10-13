import os
import json
import re
from difflib import SequenceMatcher

def similaridad(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def cruzar_arr_con_kobo():
    print("=" * 70)
    print("CRUCE Y COMPARACIÓN: CAMPOS A.R.R. vs ENCUESTA KOBOTOOLBOX")
    print("=" * 70)

    # 1. Cargar Kobo survey
    from conectores import KoboToolboxConnector
    kobo = KoboToolboxConnector()
    form = kobo.obtener_formulario()
    kobo_survey = form.get("content", {}).get("survey", [])
    
    kobo_preguntas = []
    for q in kobo_survey:
        lbl = q.get("label")
        if isinstance(lbl, list) and len(lbl) > 0:
            lbl = lbl[0]
        elif not isinstance(lbl, str):
            lbl = ""
        lbl = lbl.strip()
        q_type = q.get("type", "")
        if lbl and q_type not in ["start", "end", "today", "username", "begin_group", "end_group", "begin_score", "end_score"]:
            kobo_preguntas.append({
                "name": q.get("name"),
                "type": q_type,
                "label": lbl
            })
    print(f"Preguntas activas en Kobo (filtradas sin metadatos): {len(kobo_preguntas)}")

    # 2. Cargar ARR
    arr_json = r"d:\08_Ciclo\03_Practicas_Preprofesionales\lake\processed\campos_arr.json"
    with open(arr_json, "r", encoding="utf-8") as f:
        arr_items = json.load(f)
    print(f"Campos totales en A.R.R.: {len(arr_items)}")

    # 3. Categorización temática de ARR
    # Agrupar campos ARR por temas
    categorias_arr = {
        "1. Demografía y Población (Cap 1-3)": [],
        "2. Accesibilidad, Vías y Transporte (Cap 4, 7)": [],
        "3. Educación y Desarrollo Infantil (Cap 5)": [],
        "4. Salud y Establecimientos (Cap 6)": [],
        "5. Servicios Básicos e Infraestructura (Cap 8, 9)": [],
        "6. Economía, Producción y Suelo (Cap 10-15)": [],
        "7. Medio Ambiente y Riesgos (Cap 16, 17)": [],
        "8. Turismo y Equipamientos Especiales (Cap 18)": [],
        "9. Apoyo Institucional, Municipio y Comunidad (Cap 19-22)": []
    }

    for item in arr_items:
        txt = item["texto"]
        # Asignar a categoría según prefijo o palabra clave
        m = re.match(r"^(\d+)\.", txt)
        num = int(m.group(1)) if m else 0
        
        if num in [1, 2, 3]:
            categorias_arr["1. Demografía y Población (Cap 1-3)"].append(txt)
        elif num in [4, 7]:
            categorias_arr["2. Accesibilidad, Vías y Transporte (Cap 4, 7)"].append(txt)
        elif num == 5 or "educa" in txt.lower() or "escuela" in txt.lower():
            categorias_arr["3. Educación y Desarrollo Infantil (Cap 5)"].append(txt)
        elif num == 6 or "salud" in txt.lower():
            categorias_arr["4. Salud y Establecimientos (Cap 6)"].append(txt)
        elif num in [8, 9] or "agua" in txt.lower() or "energ" in txt.lower():
            categorias_arr["5. Servicios Básicos e Infraestructura (Cap 8, 9)"].append(txt)
        elif num in [10, 11, 12, 13, 14, 15]:
            categorias_arr["6. Economía, Producción y Suelo (Cap 10-15)"].append(txt)
        elif num in [16, 17] or "ambiente" in txt.lower() or "daño" in txt.lower():
            categorias_arr["7. Medio Ambiente y Riesgos (Cap 16, 17)"].append(txt)
        elif num == 18:
            categorias_arr["8. Turismo y Equipamientos Especiales (Cap 18)"].append(txt)
        else:
            categorias_arr["9. Apoyo Institucional, Municipio y Comunidad (Cap 19-22)"].append(txt)

    # 4. Cruzar coincidencias temáticas y semánticas
    coincidencias = []
    
    # Palabras clave clave en Kobo
    for kp in kobo_preguntas:
        k_txt = kp["label"].lower()
        mejor_match = None
        max_sim = 0
        
        for item in arr_items:
            a_txt = item["texto"].lower()
            
            # Coincidencias temáticas explícitas
            temas_comunes = [
                ("agua", ["agua", "red de agua"]),
                ("alcantarillado", ["alcantarillado", "descarga"]),
                ("electricidad", ["electricidad", "energía"]),
                ("basura", ["basura", "desecho", "recolección"]),
                ("vía", ["vía", "camino", "acceso", "transporte"]),
                ("techo", ["techo"]),
                ("piso", ["piso"]),
                ("pared", ["pared"]),
                ("étnico", ["étnico", "cultura", "costumbre"]),
                ("edad", ["edad", "años"]),
                ("sexo", ["sexo", "género"]),
                ("trabajo", ["trabajo", "ocupación", "actividad"]),
                ("ingreso", ["ingreso", "sueldo"]),
                ("ambiente", ["ambiente", "recicla", "contamina"]),
                ("municipio", ["municipio", "gobierno"]),
                ("comunidad", ["comunidad", "barrio"]),
                ("seguridad", ["policía", "robo", "crimen", "justicia"])
            ]
            
            for tag, kws in temas_comunes:
                if any(kw in k_txt for kw in kws) and any(kw in a_txt for kw in kws):
                    sim = 0.7 + (similaridad(k_txt, a_txt) * 0.3)
                    if sim > max_sim:
                        max_sim = sim
                        mejor_match = item["texto"]
                        
        if mejor_match and max_sim > 0.65:
            coincidencias.append({
                "kobo_pregunta": kp["label"],
                "kobo_tipo": kp["type"],
                "arr_campo": mejor_match,
                "score": round(max_sim, 2)
            })

    # Guardar reporte de cruce en Markdown
    reporte_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\lake\processed\cruce_preguntas_arr_vs_kobo.md"
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("# Informe Técnico de Cruce Metodológico: Ficha A.R.R. vs Encuesta KoboToolbox\n\n")
        f.write("Diagnóstico Territorial y Comunitario — Barrio El Capulí (Punzara, Loja)\n\n")
        f.write("---\n\n")
        f.write("## 1. Naturaleza Metodológica de Ambos Instrumentos\n\n")
        f.write("| Dimensión | Ficha A.R.R. (`CAMPOS ARR.xls`) | Encuesta KoboToolbox (`encuesta capuli arquitectura`) |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write("| **Nivel de Observación** | **Mesotorritorial / Comunitario (Líderes, Ficha Barrial)** | **Microterritorial / Hogar (Familias e Individuos)** |\n")
        f.write("| **Informante Clave** | Presidente del Barrio, Directiva, Personal de Salud/Escuela | Jefe de Hogar / Morador encuestado |\n")
        f.write("| **Propósito** | Inventario físico de equipamientos, vías, escuelas y servicios | Condiciones de habitabilidad, necesidades básicas y percepción |\n")
        f.write("| **Total de Variables** | 386 campos temáticos (22 capítulos) | 115 variables estructuradas |\n\n")
        f.write("---\n\n")
        f.write("## 2. Preguntas que se Cruzan Directamente (Coincidencias Clave)\n\n")
        f.write("Estas preguntas miden la misma variable y deben mantenerse consistentes entre la ficha del líder barrial y la encuesta de hogar:\n\n")
        f.write("| Variable Territorial | Pregunta en Encuesta Kobo (Hogar) | Campo Homólogo en Ficha A.R.R. (Comunidad) |\n")
        f.write("| :--- | :--- | :--- |\n")
        for c in coincidencias[:25]:
            f.write(f"| `{c['kobo_tipo']}` | {c['kobo_pregunta']} | {c['arr_campo']} |\n")
        f.write("\n---\n\n")
        f.write("## 3. Estructura de Capítulos de la Ficha A.R.R. (386 campos)\n\n")
        for cat, items in categorias_arr.items():
            f.write(f"### {cat} ({len(items)} campos)\n")
            for it in items[:6]:
                f.write(f"- {it}\n")
            if len(items) > 6:
                f.write(f"- *... y {len(items)-6} campos adicionales.*\n")
            f.write("\n")

    print(f"Informe de cruce guardado exitosamente en:\n{reporte_path}")

if __name__ == "__main__":
    cruzar_arr_con_kobo()
