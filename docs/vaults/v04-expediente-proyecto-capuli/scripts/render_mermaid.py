import base64
import json
import urllib.request
import os

mermaid_code = """gantt
    title Cronograma de Asistencia Técnica y Aceleración (CIS II - GIZ)
    dateFormat  X
    axisFormat Mes %s
    
    section Paquete 1: Ingeniería
    Topografía de detalle y geotecnia en lotes municipales :active, p1, 0, 2
    Modelación hidrológica de biofiltros y SUDs             :p2, 1, 3
    
    section Paquete 2: Financiero
    Elaboración de APUs y presupuesto definitivo            :p3, 2, 4
    Estructuración de modelo CAPEX + OPEX bancable          :p4, 3, 5
    
    section Paquete 3: Habilitantes
    Ficha y categorización ambiental MAATE / GAD            :p5, 2, 5
    Certificación catastral y fajas de protección           :p6, 1, 3
    
    section Paquete 4: Bancabilidad
    Carpeta final para financiamiento BDE / Fondos Verdes   :p7, 4, 6
"""

# Save .mmd file first
mmd_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\assets\ruta_critica_aceleracion.mmd"
with open(mmd_path, "w", encoding="utf-8") as f:
    f.write(mermaid_code)
print(f"Saved mermaid definition to {mmd_path}")

# Mermaid.ink accepts base64 encoded json or base64 encoded string
# Using mermaid.ink API: https://mermaid.ink/img/<base64>
graph_state = {
    "code": mermaid_code,
    "mermaid": {"theme": "default"}
}
json_bytes = json.dumps(graph_state).encode('utf-8')
base64_str = base64.urlsafe_b64encode(json_bytes).decode('ascii')

url = f"https://mermaid.ink/img/{base64_str}?bgColor=!white"
print(f"Fetching from {url}")

req = urllib.request.Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)

png_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\assets\ruta_critica_aceleracion.png"
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()
    with open(png_path, "wb") as f:
        f.write(data)

print(f"Successfully generated PNG at {png_path} ({len(data)} bytes)")
