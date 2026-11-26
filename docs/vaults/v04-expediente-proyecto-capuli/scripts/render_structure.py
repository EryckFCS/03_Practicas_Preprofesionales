import base64
import json
import urllib.request

mermaid_code = """flowchart TD
    A["<b>PROYECTO EL CAPULÍ: ARQUITECTURA MODULAR POR PRELACIÓN</b><br>(Inversión estimada referencial: USD 1.250.000,00 ± 20% sin IVA)"]
    
    A --> B["<b>NIVEL 1: NÚCLEO PRIORITARIO</b><br>Recuperación ribereña y control de escorrentía"]
    A --> C["<b>NIVEL 2: ACCESO Y USO SEGURO</b><br>Conectividad peatonal y pacificación vial"]
    A --> D["<b>NIVEL 3: COMPLEMENTOS CONDICIONADOS</b><br>Sujetos a validación técnica y operativa"]
    
    B --> B1["<b>C1. Parque Fluvial y Bioingeniería</b><br>19.513,57 m² en predios municipales<br>(Claves 1101500220083 y 1101500220086)"]
    B --> B2["<b>C3. Drenaje Sostenible Controlado (SUDs)</b><br>8 celdas de laminación y retención impermeabilizada<br>precautoria en tramos de ladera susceptible"]
    
    C --> C1["<b>C2a. Accesibilidad Universal 8-80</b><br>2,40 km priorizados sobre 9,64 km de red<br>Aceras continuas, vados y lote 1101020202110024"]
    
    D --> D1["<b>C4. Alumbrado Solar Off-Grid</b><br>120 luminarias LED 60W con dimming<br>Batería LiFePO4 1.280 Wh (~2,5 noches)"]
    D --> D2["<b>C2b. Ciclorruta Conectora</b><br>Sujeta a verificación de sección vial<br>hacia nodo universitario La Argelia"]
    D --> D3["<b>C5. Piloto de Biomasa y Compostaje</b><br>3 puntos limpios y módulo comunal<br>(sujeto a estudio de residuos y operador)"]

    style A fill:#1a365d,stroke:#0f172a,stroke-width:2px,color:#ffffff
    style B fill:#1e40af,stroke:#1e3a8a,stroke-width:2px,color:#ffffff
    style C fill:#0f766e,stroke:#115e59,stroke-width:2px,color:#ffffff
    style D fill:#475569,stroke:#334155,stroke-width:2px,color:#ffffff
    style B1 fill:#eff6ff,stroke:#93c5fd,stroke-width:1px,color:#1e3a8a
    style B2 fill:#eff6ff,stroke:#93c5fd,stroke-width:1px,color:#1e3a8a
    style C1 fill:#f0fdf4,stroke:#86efac,stroke-width:1px,color:#14532d
    style D1 fill:#f8fafc,stroke:#cbd5e1,stroke-width:1px,color:#334155
    style D2 fill:#f8fafc,stroke:#cbd5e1,stroke-width:1px,color:#334155
    style D3 fill:#f8fafc,stroke:#cbd5e1,stroke-width:1px,color:#334155
"""

mmd_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\assets\estructura_proyecto_cinco_sectores.mmd"
with open(mmd_path, "w", encoding="utf-8") as f:
    f.write(mermaid_code)

graph_state = {
    "code": mermaid_code,
    "mermaid": {"theme": "default"}
}
json_bytes = json.dumps(graph_state).encode('utf-8')
base64_str = base64.urlsafe_b64encode(json_bytes).decode('ascii')

url = f"https://mermaid.ink/img/{base64_str}?bgColor=!white"

req = urllib.request.Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

png_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\assets\estructura_proyecto_cinco_sectores.png"
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()
    with open(png_path, "wb") as f:
        f.write(data)

print(f"Exported {png_path} ({len(data)} bytes)")
