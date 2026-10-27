import os
import pandas as pd

output_dir = "plantillas_xlsform"
os.makedirs(output_dir, exist_ok=True)

# ==============================================================================
# 1. PLANTILLA: LEVANTAMIENTO TERRITORIAL Y PREDIAL
# ==============================================================================
survey_p1 = [
    {"type": "start", "name": "inicio", "label": "", "required": "", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "end", "name": "fin", "label": "", "required": "", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "text", "name": "cod_brigada", "label": "Código o Nombre del Investigador / Brigada", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "text", "name": "sector_estudio", "label": "Nombre del Sector, Barrio o Zona de Estudio", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "geopoint", "name": "ubicacion_gps", "label": "Coordenada Satelital GPS del Predio (Esperar precisión <= 5m)", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one estado_lote_list", "name": "estado_lote", "label": "Estado Físico del Lote / Predio", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "decimal", "name": "frente_lote_m", "label": "Dimensión del frente del lote hacia la vía (metros)", "required": "yes", "constraint": ". >= 3.0 and . <= 120.0", "constraint_message": "Error: El frente debe estar entre 3.0 m y 120.0 m", "relevant": ""},
    {"type": "decimal", "name": "fondo_lote_m", "label": "Dimensión aproximada del fondo del lote (metros)", "required": "no", "constraint": ". >= 5.0 and . <= 200.0", "constraint_message": "Error: El fondo debe estar entre 5.0 m y 200.0 m", "relevant": ""},
    {"type": "select_one topografia_list", "name": "topografia", "label": "Topografía y Pendiente Predominante del Terreno", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "image", "name": "foto_fachada", "label": "Fotografía Técnica de Fachada Frontal (Horizontal)", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "note", "name": "nota_cierre", "label": "Verifique que los datos periciales concuerden con la observación física antes de guardar.", "required": "", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "text", "name": "observaciones_campo", "label": "Observaciones Técnicas Generales del Perito", "required": "no", "constraint": "", "constraint_message": "", "relevant": ""}
]

choices_p1 = [
    {"list_name": "estado_lote_list", "name": "baldio", "label": "Lote Baldío / Desocupado"},
    {"list_name": "estado_lote_list", "name": "construido", "label": "Edificación Terminada y Ocupada"},
    {"list_name": "estado_lote_list", "name": "en_construccion", "label": "Obra Gris o en Proceso de Construcción"},
    {"list_name": "estado_lote_list", "name": "abandonado", "label": "Estructura Abandonada / Inhabitable"},
    {"list_name": "topografia_list", "name": "plano", "label": "Terreno Plano (Pendiente < 5%)"},
    {"list_name": "topografia_list", "name": "pendiente_suave", "label": "Pendiente Suave (5% - 15%)"},
    {"list_name": "topografia_list", "name": "pendiente_media", "label": "Pendiente Moderada (16% - 30%)"},
    {"list_name": "topografia_list", "name": "pendiente_abrupta", "label": "Pendiente Fuerte / Quebrada (> 30%)"}
]

settings_p1 = [
    {"form_title": "Plantilla 01 - Ficha Levantamiento Territorial y Predial", "form_id": "ficha_territorial_unl_2026", "version": "202601"}
]

# ==============================================================================
# 2. PLANTILLA: INSPECCIÓN CONSTRUCTIVA, PATOLOGÍAS Y VIDEO
# ==============================================================================
survey_p2 = [
    {"type": "start", "name": "inicio", "label": "", "required": "", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "text", "name": "cod_predio", "label": "Identificador o Clave Catastral / Código de Manzana-Lote", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "geopoint", "name": "coordenada_edificacion", "label": "Punto GPS del Acceso Principal", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "integer", "name": "num_pisos", "label": "Número de Pisos Construidos sobre nivel de acera", "required": "yes", "constraint": ". >= 1 and . <= 8", "constraint_message": "Error: Número de pisos admisible entre 1 y 8 niveles", "relevant": ""},
    {"type": "select_one sistema_estructural_list", "name": "sistema_estructural", "label": "Sistema Estructural Predominante", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one tipo_cubierta_list", "name": "tipo_cubierta", "label": "Tipo de Cubierta / Techo", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one estado_conservacion_list", "name": "estado_conservacion", "label": "Estado General de Conservación de la Estructura", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one si_no_list", "name": "presenta_dano", "label": "¿Presenta patologías visibles o indicios de daño estructural?", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_multiple patologias_list", "name": "patologias_detectadas", "label": "Seleccione las Patologías Visibles en la Edificación", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${presenta_dano} = 'si'"},
    {"type": "image", "name": "foto_patologia", "label": "Fotografía en Detalle del Daño o Fisura Estructural", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${presenta_dano} = 'si'"},
    {"type": "video", "name": "video_pericial_15s", "label": "Video Pericial de Entorno y Estructura (Máx. 15 segundos en paneo lento)", "required": "no", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "text", "name": "dictamen_tecnico", "label": "Diagnóstico Técnico Preliminar del Evaluador", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""}
]

choices_p2 = [
    {"list_name": "sistema_estructural_list", "name": "porticos_hormigon", "label": "Pórticos de Hormigón Armado"},
    {"list_name": "sistema_estructural_list", "name": "mamposteria_confinada", "label": "Mampostería Confinada de Ladrillo/Bloque"},
    {"list_name": "sistema_estructural_list", "name": "estructura_metalica", "label": "Perfiles y Columnas Metálicas"},
    {"list_name": "sistema_estructural_list", "name": "madera", "label": "Estructura de Madera Tratada"},
    {"list_name": "sistema_estructural_list", "name": "adobe_tapial", "label": "Adobe Tradicional / Tapial"},
    {"list_name": "sistema_estructural_list", "name": "mixto", "label": "Sistema Mixto o Autoconstrucción Empírica"},
    {"list_name": "tipo_cubierta_list", "name": "losa_hormigon", "label": "Losa Plana / Inclinada de Hormigón"},
    {"list_name": "tipo_cubierta_list", "name": "teja_artesanal", "label": "Teja Cerámica sobre Cerchas"},
    {"list_name": "tipo_cubierta_list", "name": "zinc_fibrocemento", "label": "Planchas de Zinc / Fibrocemento"},
    {"list_name": "tipo_cubierta_list", "name": "otra", "label": "Otro Material"},
    {"list_name": "estado_conservacion_list", "name": "bueno", "label": "Bueno (Sin daños aparentes)"},
    {"list_name": "estado_conservacion_list", "name": "regular", "label": "Regular (Fisuras superficiales / acabado deteriorado)"},
    {"list_name": "estado_conservacion_list", "name": "malo", "label": "Malo (Grietas activas o desprendimientos)"},
    {"list_name": "estado_conservacion_list", "name": "riesgo_inminente", "label": "Riesgo de Colapso / Evacuación recomendada"},
    {"list_name": "si_no_list", "name": "si", "label": "Sí"},
    {"list_name": "si_no_list", "name": "no", "label": "No"},
    {"list_name": "patologias_list", "name": "grieta_diagonal_45", "label": "Fisuras diagonales a 45° en mampostería (Asentamiento / Sismo)"},
    {"list_name": "patologias_list", "name": "desprendimiento_recubrimiento", "label": "Armadura vista / Acero corroído en columnas/vigas"},
    {"list_name": "patologias_list", "name": "humedad_capilaridad", "label": "Humedad ascendente por capilaridad en base de muros"},
    {"list_name": "patologias_list", "name": "flecha_excesiva", "label": "Deformación o flecha excesiva en vigas o losas"},
    {"list_name": "patologias_list", "name": "socavacion_cimentacion", "label": "Pérdida de suelo o socavación en cimientos"}
]

settings_p2 = [
    {"form_title": "Plantilla 02 - Ficha de Inspección Constructiva y Patologías", "form_id": "ficha_constructiva_unl_2026", "version": "202601"}
]

# ==============================================================================
# 3. PLANTILLA: ENCUESTA SOCIOECONÓMICA Y DE SERVICIOS PÚBLICOS
# ==============================================================================
survey_p3 = [
    {"type": "start", "name": "inicio", "label": "", "required": "", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one si_no_list", "name": "consentimiento_informado", "label": "Consentimiento Verbal: ¿Acepta participar voluntariamente en esta encuesta académica?", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "geopoint", "name": "ubicacion_hogar", "label": "Punto Satelital GPS de la Vivienda", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one tenencia_list", "name": "tenencia_vivienda", "label": "Régimen de Tenencia del Inmueble", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_informado} = 'si'"},
    {"type": "integer", "name": "num_habitantes", "label": "Número de personas que residen permanentemente en este hogar", "required": "yes", "constraint": ". >= 1 and . <= 18", "constraint_message": "Error: Ingrese un valor válido entre 1 y 18 personas", "relevant": "${consentimiento_informado} = 'si'"},
    {"type": "select_multiple servicios_list", "name": "servicios_basicos", "label": "Seleccione los Servicios Básicos con los que cuenta la vivienda", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_informado} = 'si'"},
    {"type": "select_one continuidad_agua_list", "name": "continuidad_agua", "label": "Frecuencia de suministro del servicio de Agua Potable", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "selected(${servicios_basicos}, 'agua_red') and ${consentimiento_informado} = 'si'"},
    {"type": "select_one prioridad_list", "name": "necesidad_prioritaria", "label": "¿Cuál considera que es la obra o necesidad más urgente para este sector?", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_informado} = 'si'"},
    {"type": "audio", "name": "audio_testimonio_necesidad", "label": "Grabación en Audio de la Justificación del Morador (30 seg)", "required": "no", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_informado} = 'si'"}
]

choices_p3 = [
    {"list_name": "si_no_list", "name": "si", "label": "Sí (Acepta voluntariamente)"},
    {"list_name": "si_no_list", "name": "no", "label": "No (Rechaza la encuesta)"},
    {"list_name": "tenencia_list", "name": "propia_con_titulo", "label": "Propia (con escritura / título inscrito)"},
    {"list_name": "tenencia_list", "name": "propia_posesion", "label": "Propia en posesión (sin escritura legal)"},
    {"list_name": "tenencia_list", "name": "arrendada", "label": "Arrendada / Alquiler"},
    {"list_name": "tenencia_list", "name": "prestada_familiar", "label": "Cedida por familiar / Guardián"},
    {"list_name": "servicios_list", "name": "agua_red", "label": "Red pública de agua potable"},
    {"list_name": "servicios_list", "name": "alcantarillado", "label": "Red pública de alcantarillado sanitario"},
    {"list_name": "servicios_list", "name": "energia", "label": "Red eléctrica pública formal con medidor"},
    {"list_name": "servicios_list", "name": "recoleccion_basura", "label": "Servicio municipal de recolección de desechos"},
    {"list_name": "servicios_list", "name": "internet", "label": "Conexión a internet fijo o fibra óptica"},
    {"list_name": "continuidad_agua_list", "name": "continuo_24h", "label": "Servicio continuo las 24 horas del día"},
    {"list_name": "continuidad_agua_list", "name": "interdiario", "label": "Por días alternos / interdiario"},
    {"list_name": "continuidad_agua_list", "name": "pocas_horas", "label": "Solo unas pocas horas al día"},
    {"list_name": "continuidad_agua_list", "name": "tanquero", "label": "Por tanquero o acarreo manual"},
    {"list_name": "prioridad_list", "name": "vialidad_asfalto", "label": "Vialidad, adoquinado y aceras seguras"},
    {"list_name": "prioridad_list", "name": "alcantarillado_pluvial", "label": "Drenaje pluvial y mitigación de inundaciones"},
    {"list_name": "prioridad_list", "name": "alumbrado_seguridad", "label": "Alumbrado público y seguridad ciudadana"},
    {"list_name": "prioridad_list", "name": "espacio_verde", "label": "Parque infantil, canchas o áreas recreativas"},
    {"list_name": "prioridad_list", "name": "equipamiento_salud", "label": "Puesto de salud o guardería comunitaria"}
]

settings_p3 = [
    {"form_title": "Plantilla 03 - Encuesta Socioeconómica y Servicios Básicos", "form_id": "encuesta_socioeconomica_unl_2026", "version": "202601"}
]

# ==============================================================================
# 4. PLANTILLA: ENTREVISTA CUALITATIVA A INFORMANTE CLAVE CON AUDIO
# ==============================================================================
survey_p4 = [
    {"type": "start", "name": "inicio", "label": "", "required": "", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one si_no_list", "name": "consentimiento_grabacion", "label": "Consentimiento Expreso: ¿Autoriza la grabación en audio de su testimonio con fines de investigación académica?", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "geopoint", "name": "coordenada_entrevista", "label": "Ubicación del Encuentro / Entrevista", "required": "yes", "constraint": "", "constraint_message": "", "relevant": ""},
    {"type": "select_one actor_list", "name": "perfil_actor", "label": "Perfil del Informante Territorial Clave", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_grabacion} = 'si'"},
    {"type": "integer", "name": "tiempo_residencia", "label": "¿Cuántos años lleva residiendo o trabajando en este territorio?", "required": "yes", "constraint": ". >= 1 and . <= 90", "constraint_message": "Error: Ingrese un tiempo de residencia coherente (1 a 90 años)", "relevant": "${consentimiento_grabacion} = 'si'"},
    {"type": "audio", "name": "audio_historia_fundacion", "label": "Audio 1 (1-2 min): Memoria Histórica del Barrio y Eventos Hidrogeológicos Pasados", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_grabacion} = 'si'"},
    {"type": "audio", "name": "audio_problemas_constructivos", "label": "Audio 2 (1-2 min): Problemas Constructivos, Calidad de Suelos y Obras Inconclusas", "required": "no", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_grabacion} = 'si'"},
    {"type": "text", "name": "sintesis_pericial_investigador", "label": "Síntesis Analítica y Juicio Cualitativo del Investigador", "required": "yes", "constraint": "", "constraint_message": "", "relevant": "${consentimiento_grabacion} = 'si'"}
]

choices_p4 = [
    {"list_name": "si_no_list", "name": "si", "label": "Sí (Autoriza grabación)"},
    {"list_name": "si_no_list", "name": "no", "label": "No (Rechaza grabación)"},
    {"list_name": "actor_list", "name": "dirigente_barrial", "label": "Dirigente o Presidente Barrial"},
    {"list_name": "actor_list", "name": "fundador_adulto_mayor", "label": "Adulto Mayor / Morador Fundador"},
    {"list_name": "actor_list", "name": "maestro_obra", "label": "Maestro de Obra / Albañil del sector"},
    {"list_name": "actor_list", "name": "comerciante_local", "label": "Comerciante / Emprendedor local"},
    {"list_name": "actor_list", "name": "tecnico_institucional", "label": "Técnico del GAD o Empresa Pública"}
]

settings_p4 = [
    {"form_title": "Plantilla 04 - Entrevista Cualitativa a Informante Clave", "form_id": "entrevista_cualitativa_unl_2026", "version": "202601"}
]

# Guardar los 4 archivos Excel en la carpeta plantillas_xlsform
files = [
    ("plantillas_xlsform/01_plantilla_levantamiento_territorial.xlsx", survey_p1, choices_p1, settings_p1),
    ("plantillas_xlsform/02_plantilla_inspeccion_constructiva_patologias.xlsx", survey_p2, choices_p2, settings_p2),
    ("plantillas_xlsform/03_plantilla_encuesta_socioeconomica_servicios.xlsx", survey_p3, choices_p3, settings_p3),
    ("plantillas_xlsform/04_plantilla_entrevista_cualitativa_audio.xlsx", survey_p4, choices_p4, settings_p4)
]

for filename, s, c, st in files:
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        pd.DataFrame(s).to_excel(writer, sheet_name="survey", index=False)
        pd.DataFrame(c).to_excel(writer, sheet_name="choices", index=False)
        pd.DataFrame(st).to_excel(writer, sheet_name="settings", index=False)
    print(f"Creado con éxito: {filename}")
