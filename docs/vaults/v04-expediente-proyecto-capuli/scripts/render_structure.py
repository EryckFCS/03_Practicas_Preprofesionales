import base64
import json
import urllib.request

mermaid_code = """flowchart TD
    A["<b>PROYECTO INTEGRAL EL CAPULÍ</b><br>(Presupuesto referencial: USD 1.250.000,00)"]
    
    A --> B["<b>SECTOR PRINCIPAL ELEGIBLE</b><br>Espacio público y recuperación del espacio natural"]
    A --> C["<b>COMPONENTES COMPLEMENTARIOS</b><br>Desempeño en criterios de priorización CIS II"]
    
    B --> B1["Parque Fluvial río Capulí<br>(1,45 ha suelo municipal)"]
    B --> B2["Corredor de movilidad activa 8-80<br>(2,4 km de senderos y ciclorruta)"]
    B --> B3["Fijación de laderas con bioingeniería<br>(Soluciones basadas en la Naturaleza)"]
    
    C --> C1["Eficiencia hídrica y resiliencia<br>(8 biofiltros y red SUDs)"]
    C --> C2["Eficiencia y energía renovable<br>(120 luminarias solares autónomas)"]
    C --> C3["Gestión de residuos y circularidad<br>(Puntos limpios y compostera barrial)"]

    style A fill:#1a365d,stroke:#0f172a,stroke-width:2px,color:#ffffff
    style B fill:#2b6cb0,stroke:#1e3a8a,stroke-width:2px,color:#ffffff
    style C fill:#2c7a7b,stroke:#134e4a,stroke-width:2px,color:#ffffff
    style B1 fill:#edf2f7,stroke:#cbd5e0,stroke-width:1px,color:#1a202c
    style B2 fill:#edf2f7,stroke:#cbd5e0,stroke-width:1px,color:#1a202c
    style B3 fill:#edf2f7,stroke:#cbd5e0,stroke-width:1px,color:#1a202c
    style C1 fill:#f0fdf4,stroke:#bbf7d0,stroke-width:1px,color:#14532d
    style C2 fill:#fefce8,stroke:#fef08a,stroke-width:1px,color:#713f12
    style C3 fill:#eff6ff,stroke:#bfdbfe,stroke-width:1px,color:#1e3a8a
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
