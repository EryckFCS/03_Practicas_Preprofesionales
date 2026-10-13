"""
Script de Optimización y Poda Metodológica para la Encuesta KoboToolbox:
'encuesta capuli arquitectura' (UID: aBJEiLwrvSWwb7fBrukk8a)

Acciones:
1. Poda: Elimina preguntas de confianza judicial y penitenciaria (Justicia, Fiscalía, Defensoría, Cárceles).
2. Incorporación de campos A.R.R. para Arquitectura y Urbanismo:
   - Fotografía de la fachada de la vivienda (tipo: image).
   - Tenencia detallada (Propia con escrituras vs Posesión informal sin escrituras vs Arriendo).
   - Movilidad y tiempo de traslado al campus La Argelia (UNL) / Centro de Loja.
   - Riesgo ambiental y cercanía a quebradas / deslizamientos de talud.
   - Equipamiento comunitario existente (parques, canchas, casa comunal).
3. Actualización y Redeploy automático en KoboToolbox API v2.
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

def optimizar_encuesta():
    print("=" * 70)
    print("OPTIMIZACIÓN METODOLÓGICA DE ENCUESTA KOBOTOOLBOX — EL CAPULÍ")
    print("=" * 70)

    kobo = KoboToolboxConnector()
    form = kobo.obtener_formulario()
    content = form.get("content", {})
    survey = content.get("survey", [])
    choices = content.get("choices", [])

    print(f"Estado inicial: {len(survey)} preguntas en survey, {len(choices)} opciones en choices.")

    # ---------------------------------------------------------
    # 1. PODA: Filtrar preguntas judiciales irrelevantes
    # ---------------------------------------------------------
    preguntas_a_eliminar = [
        "administración de justicia",
        "fiscalia general del estado",
        "defensoría pública",
        "sistema de rehabilitación social"
    ]

    survey_filtrado = []
    podadas = 0

    for q in survey:
        lbl = q.get("label", [])
        lbl_str = lbl[0].lower() if isinstance(lbl, list) and len(lbl) > 0 else str(lbl).lower()
        
        # Comprobar si coincide con alguna a podar
        if any(term in lbl_str for term in preguntas_a_eliminar):
            print(f" [- PODA] Eliminada: {lbl_str[:60]}...")
            podadas += 1
            continue
            
        # Renombrar grupo de seguridad ciudadana para quitar "justicia"
        if q.get("name") == "group_wu5xu07" and q.get("type") == "begin_group":
            q["label"] = ["Seguridad ciudadana en el barrio"]
            
        survey_filtrado.append(q)

    print(f"Total preguntas podadas: {podadas}")

    # ---------------------------------------------------------
    # 2. ACTUALIZAR LISTA DE TENENCIA (ak8wx06)
    # ---------------------------------------------------------
    choices_actualizados = []
    for c in choices:
        if c.get("list_name") == "ak8wx06":
            # Reemplazaremos esta lista con opciones más detalladas de tenencia
            continue
        choices_actualizados.append(c)

    # Nuevas opciones de tenencia con distinción formal/informal
    opciones_tenencia = [
        ("1", "Propia con escrituras legalizadas"),
        ("2", "En posesión o herencia familiar (sin escrituras legalizadas)"),
        ("3", "Arrendada (alquiler)"),
        ("4", "Prestada o cedida"),
        ("5", "Otra situación")
    ]
    for val, texto in opciones_tenencia:
        choices_actualizados.append({
            "name": val,
            "label": [texto],
            "list_name": "ak8wx06",
            "$kuid": gen_kuid(),
            "$autovalue": val
        })

    # ---------------------------------------------------------
    # 3. CREAR NUEVAS LISTAS DE OPCIONES PARA ARQUITECTURA / A.R.R.
    # ---------------------------------------------------------
    # Lista de Medios de Transporte
    list_transporte = "list_transporte_arr"
    opciones_transporte = [
        ("1", "A pie (caminando)"),
        ("2", "Bus de transporte urbano"),
        ("3", "Taxi / Camioneta"),
        ("4", "Automóvil particular propio"),
        ("5", "Motocicleta"),
        ("6", "Bicicleta")
    ]
    for val, texto in opciones_transporte:
        choices_actualizados.append({
            "name": val,
            "label": [texto],
            "list_name": list_transporte,
            "$kuid": gen_kuid(),
            "$autovalue": val
        })

    # Lista de Riesgos y Quebradas
    list_riesgo = "list_riesgo_quebrada"
    opciones_riesgo = [
        ("1", "Sí, riesgo de inundación o desborde de quebrada"),
        ("2", "Sí, riesgo de deslizamiento o caída de talud"),
        ("3", "No, la vivienda se encuentra en terreno plano y estable"),
        ("4", "No sabe / No responde")
    ]
    for val, texto in opciones_riesgo:
        choices_actualizados.append({
            "name": val,
            "label": [texto],
            "list_name": list_riesgo,
            "$kuid": gen_kuid(),
            "$autovalue": val
        })

    # Lista de Equipamiento Comunitario
    list_equipamiento = "list_equipamiento_barrio"
    opciones_equipamiento = [
        ("1", "Sí, en buen estado y accesible"),
        ("2", "Sí, pero se encuentra deteriorado o abandonado"),
        ("3", "No existe ningún espacio público en el sector"),
        ("4", "No sabe")
    ]
    for val, texto in opciones_equipamiento:
        choices_actualizados.append({
            "name": val,
            "label": [texto],
            "list_name": list_equipamiento,
            "$kuid": gen_kuid(),
            "$autovalue": val
        })

    # ---------------------------------------------------------
    # 4. INSERTAR NUEVAS PREGUNTAS EN SURVEY
    # ---------------------------------------------------------
    survey_final = []

    for q in survey_filtrado:
        # A. Dentro del grupo de Vivienda (group_tb9xo41)
        # Justo después de la descarga de aguas residuales, insertar Foto y Riesgo
        if q.get("type") == "select_one" and any("descarga de agua residuales" in str(q.get("label", "")).lower() for _ in [1]):
            survey_final.append(q)
            
            # Pregunta: Riesgo por Quebrada / Deslizamiento
            q_riesgo = {
                "type": "select_one",
                "$kuid": gen_kuid(),
                "name": "riesgo_quebrada_deslizamiento",
                "label": ["¿Su vivienda o terreno ha sufrido afectaciones o está en riesgo por desborde de quebradas o deslizamientos de tierra?"],
                "select_from_list_name": list_riesgo,
                "required": False,
                "$qpath": "group_tb9xo41-riesgo_quebrada_deslizamiento",
                "$xpath": "group_tb9xo41/riesgo_quebrada_deslizamiento"
            }
            survey_final.append(q_riesgo)
            print(" [+ AÑADIDA] Pregunta de Riesgo por quebrada / talud (Vivienda)")

            # Pregunta: Fotografía de la fachada de la vivienda
            q_foto = {
                "type": "image",
                "$kuid": gen_kuid(),
                "name": "fotografia_fachada_vivienda",
                "label": ["Fotografía de la fachada de la vivienda o entorno inmediato:"],
                "required": False,
                "$qpath": "group_tb9xo41-fotografia_fachada_vivienda",
                "$xpath": "group_tb9xo41/fotografia_fachada_vivienda"
            }
            survey_final.append(q_foto)
            print(" [+ AÑADIDA] Pregunta de Fotografía de la fachada (tipo: image)")
            continue

        survey_final.append(q)

    # B. Insertar un bloque temático de Movilidad Urbana y Equipamiento
    # Justo antes del grupo de Felicidad o al final de vivienda
    idx_insert = -1
    for i, q in enumerate(survey_final):
        if q.get("name") == "group_vz2xh95" and q.get("type") == "begin_group":
            idx_insert = i
            break

    bloque_movilidad = [
        {
            "type": "begin_group",
            "$kuid": gen_kuid(),
            "name": "group_movilidad_equipamiento",
            "label": ["Movilidad, accesibilidad urbana y equipamiento barrial (Arquitectura / A.R.R.)"],
            "$qpath": "group_movilidad_equipamiento",
            "$xpath": "group_movilidad_equipamiento"
        },
        {
            "type": "select_one",
            "$kuid": gen_kuid(),
            "name": "medio_transporte_principal",
            "label": ["¿Cuál es el principal medio de transporte que utiliza para trasladarse a sus actividades cotidianas (UNL Campus La Argelia / Trabajo / Centro de Loja)?"],
            "select_from_list_name": list_transporte,
            "required": False,
            "$qpath": "group_movilidad_equipamiento-medio_transporte_principal",
            "$xpath": "group_movilidad_equipamiento/medio_transporte_principal"
        },
        {
            "type": "integer",
            "$kuid": gen_kuid(),
            "name": "tiempo_traslado_minutos",
            "label": ["En promedio, ¿cuántos minutos le toma llegar a su destino principal cotidiano (UNL / Centro de Loja)?"],
            "required": False,
            "$qpath": "group_movilidad_equipamiento-tiempo_traslado_minutos",
            "$xpath": "group_movilidad_equipamiento/tiempo_traslado_minutos"
        },
        {
            "type": "select_one",
            "$kuid": gen_kuid(),
            "name": "equipamiento_publico_barrial",
            "label": ["¿Cuenta su sector con algún espacio público, parque, cancha deportiva o casa comunal en funcionamiento?"],
            "select_from_list_name": list_equipamiento,
            "required": False,
            "$qpath": "group_movilidad_equipamiento-equipamiento_publico_barrial",
            "$xpath": "group_movilidad_equipamiento/equipamiento_publico_barrial"
        },
        {
            "type": "end_group",
            "$kuid": gen_kuid(),
            "$qpath": "group_movilidad_equipamiento",
            "$xpath": "group_movilidad_equipamiento"
        }
    ]

    if idx_insert != -1:
        for offset, item in enumerate(bloque_movilidad):
            survey_final.insert(idx_insert + offset, item)
        print(" [+ AÑADIDO] Bloque temático de Movilidad, Accesibilidad y Equipamiento Barrial.")
    else:
        survey_final.extend(bloque_movilidad)

    print(f"\nEstado final preparado: {len(survey_final)} preguntas en survey, {len(choices_actualizados)} opciones en choices.")

    # ---------------------------------------------------------
    # 5. ACTUALIZAR EN KOBOTOOLBOX MEDIANTE PATCH
    # ---------------------------------------------------------
    nuevo_content = {
        "survey": survey_final,
        "choices": choices_actualizados,
        "settings": content.get("settings", {"style": "theme-grid", "default_language": "Español (español)"}),
        "translated": content.get("translated", ["hint", "label"]),
        "translations": content.get("translations", ["Español (español)"])
    }

    print("\nEnviando actualización PATCH a KoboToolbox API v2...")
    res_patch = kobo.actualizar_contenido_formulario(nuevo_content)
    nueva_version = res_patch.get("version_id")
    print(f"Formulario actualizado con éxito. Nueva versión generada: {nueva_version}")

    # ---------------------------------------------------------
    # 6. REDESPLEGAR EL FORMULARIO (REDEPLOY)
    # ---------------------------------------------------------
    print("Redesplegando formulario para activar cambios en campo...")
    res_deploy = kobo.redesplegar_formulario(version_id=nueva_version)
    print("¡Formulario redesplegado y 100% activo en línea!")
    print(f"UID del Despliegue: {res_deploy.get('deployed_version_id') or nueva_version}")
    print("=" * 70)

if __name__ == "__main__":
    optimizar_encuesta()
