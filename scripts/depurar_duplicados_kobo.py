"""
Script para Eliminar Preguntas Duplicadas en KoboToolbox:
1. Elimina la pregunta duplicada de ubicación GPS en el bloque inicial ('Record your current location' vs 'Ubicación').
   Se conserva 'Ubicación' que es en español y está correctamente configurada.
2. Unifica las 7 preguntas repetidas de '¿Cuál es el año más alto que aprobó?' en una sola pregunta numérica limpia.
3. Actualiza el formulario y redespliega automáticamente mediante API v2.
"""

import sys
import os
import json
import secrets
import string

sys.path.insert(0, os.path.dirname(__file__))
from conectores import KoboToolboxConnector

def gen_kuid(length=9):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def depurar_duplicados():
    print("=" * 70)
    print("DEPURACIÓN DE PREGUNTAS DUPLICADAS EN KOBOTOOLBOX — EL CAPULÍ")
    print("=" * 70)

    kobo = KoboToolboxConnector()
    form = kobo.obtener_formulario()
    content = form.get("content", {})
    survey = content.get("survey", [])
    choices = content.get("choices", [])

    print(f"Estado inicial: {len(survey)} elementos en survey.")

    survey_limpio = []
    geopoint_encontrado = False
    educacion_agregada = False

    for idx, q in enumerate(survey):
        q_type = q.get("type")
        lbl = q.get("label", [])
        lbl_str = lbl[0].strip() if isinstance(lbl, list) and len(lbl) > 0 else str(lbl).strip()

        # 1. Caso Duplicado de Ubicación en el Bloque Inicial:
        # Si es 'Record your current location', descartarla (dejamos 'Ubicación')
        if q_type == "geopoint" and "record your current location" in lbl_str.lower():
            print(f" [- ELIMINADA DUPLICADA] Ubicación en inglés: '{lbl_str}' (KUID: {q.get('$kuid')})")
            continue

        # 2. Caso de las 7 preguntas repetidas de año de instrucción:
        if q_type == "range" and "cuál es el año más alto que aprobó" in lbl_str.lower():
            if not educacion_agregada:
                # Reemplazar la primera ocurrencia con una pregunta limpia y universal
                q_unificada = {
                    "type": "integer",
                    "$kuid": gen_kuid(),
                    "name": "anio_aprobado_nivel_instruccion",
                    "label": ["¿Cuál es el año o curso más alto que aprobó en dicho nivel de instrucción?"],
                    "hint": ["Ingrese el número del último grado, curso o año aprobado (ej: 1, 2, 3, 4, 5, 6...)"],
                    "required": False,
                    "$qpath": "group_uc9qw85-anio_aprobado_nivel_instruccion",
                    "$xpath": "group_uc9qw85/anio_aprobado_nivel_instruccion"
                }
                survey_limpio.append(q_unificada)
                educacion_agregada = True
                print(" [+ UNIFICADA] Preguntas de anio de instruccion condensadas en: 'anio_aprobado_nivel_instruccion'")
            else:
                print(f" [- ELIMINADA DUPLICADA] Ocurrencia repetida de año de instrucción: (KUID: {q.get('$kuid')})")
            continue

        survey_limpio.append(q)

    print(f"\nEstado final tras depuración: {len(survey_limpio)} elementos en survey.")
    print(f"Diferencia: {len(survey) - len(survey_limpio)} elementos duplicados o redundantes eliminados.")

    # 3. Enviar actualización PATCH a la API de KoboToolbox
    nuevo_content = {
        "survey": survey_limpio,
        "choices": choices,
        "settings": content.get("settings", {"style": "theme-grid", "default_language": "Español (español)"}),
        "translated": content.get("translated", ["hint", "label"]),
        "translations": content.get("translations", ["Español (español)"])
    }

    print("\nEnviando actualización PATCH a KoboToolbox...")
    res_patch = kobo.actualizar_contenido_formulario(nuevo_content)
    nueva_version = res_patch.get("version_id")
    print(f"Formulario depurado con éxito. Nueva versión: {nueva_version}")

    # 4. Redesplegar formulario
    print("Redesplegando formulario activo...")
    res_deploy = kobo.redesplegar_formulario(version_id=nueva_version)
    print("¡Formulario redesplegado con éxito sin duplicados!")
    print(f"UID del Despliegue: {res_deploy.get('deployed_version_id') or nueva_version}")
    print("=" * 70)

if __name__ == "__main__":
    depurar_duplicados()
