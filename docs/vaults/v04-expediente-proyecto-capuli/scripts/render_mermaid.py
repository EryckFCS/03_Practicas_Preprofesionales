import base64
import json
import urllib.request

mermaid_code = """gantt
    title Plan de Asistencia Técnica por Paquetes de Trabajo (Fase III CIS II - GIZ)
    dateFormat  X
    axisFormat Mes %s
    
    section P1: Ingeniería Legal
    Homologación catastral urbana, amojonamiento hídrico e IRU definitivo :active, p1, 0, 2
    
    section P2: Hidrológico-Geotécnico
    Topografía de detalle, suelos y evaluación de laderas (Riesgo 02/03)  :p2, 1, 3
    Modelación hidráulica y validación de infiltración/conducción SUDs    :p3, 2, 4
    
    section P3: Anteproyecto y Costos
    Diseño validado del núcleo prioritario, cómputos métricos y APUs      :p4, 3, 5
    
    section P4: Social y Operativo
    Talleres participativos, actas de veeduría y manual operativo OPEX    :p5, 1, 4
    
    section P5: Económico-Financiero
    Evaluación socioeconómica, certificación POA y carpeta BDE/Fondos     :p6, 4, 6
"""

mmd_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\assets\ruta_critica_aceleracion.mmd"
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

png_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\assets\ruta_critica_aceleracion.png"
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()
    with open(png_path, "wb") as f:
        f.write(data)

print(f"Successfully generated PNG at {png_path} ({len(data)} bytes)")
