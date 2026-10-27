import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración institucional
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -----------------------------------------------------------------------------
# 1. DIAGRAMA DE ESTRUCTURA VIAL Y BARRERA TOPOGRÁFICA (CAPÍTULO 2)
# -----------------------------------------------------------------------------
def generar_diagrama_conectividad():
    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.axis('off')

    # Caja Izquierda: Red Macro
    box_macro = patches.FancyBboxPatch((0.2, 0.5), 3.2, 2.5, boxstyle="round,pad=0.2",
                                        facecolor="#F6F6F6", edgecolor="#CC0632", linewidth=1.5)
    ax.add_patch(box_macro)
    ax.text(1.8, 2.4, "Red Vial Macro\n(Av. Reinaldo Espinosa)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#333333')
    ax.text(1.8, 1.2, "• Vía colectora primaria\n• Pavimento regular\n• Tráfico motorizado continuo\n• Carencia de aceras continuas",
            ha='center', va='center', fontsize=8.5, color='#555555')

    # Caja Centro: Barrera Topográfica
    box_barrera = patches.FancyBboxPatch((3.8, 0.9), 2.4, 1.7, boxstyle="round,pad=0.2",
                                          facecolor="#FFF0F2", edgecolor="#CC0632", linewidth=1.8, linestyle="--")
    ax.add_patch(box_barrera)
    ax.text(5.0, 2.0, "BARRERA TOPOGRÁFICA", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#CC0632')
    ax.text(5.0, 1.35, "Pendientes del 15% al 35%\nDesnivel de 230 metros\nErosión hídrica invernal",
            ha='center', va='center', fontsize=8, color='#666666')

    # Caja Derecha: Red Interna
    box_interna = patches.FancyBboxPatch((6.6, 0.5), 3.2, 2.5, boxstyle="round,pad=0.2",
                                         facecolor="#F6F6F6", edgecolor="#CC0632", linewidth=1.5)
    ax.add_patch(box_interna)
    ax.text(8.2, 2.4, "Red Interna de Ladera\n(Pasajes Capulí Loma)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#333333')
    ax.text(8.2, 1.2, "• Pasajes de tierra y lastre\n• Sin obras de confinamiento\n• Sin transporte público formal\n• Aislamiento de grupos vulnerables",
            ha='center', va='center', fontsize=8.5, color='#555555')

    # Flechas conectoras
    ax.annotate('', xy=(3.8, 1.75), xytext=(3.4, 1.75),
                arrowprops=dict(arrowstyle="<->", color="#CC0632", lw=2))
    ax.annotate('', xy=(6.6, 1.75), xytext=(6.2, 1.75),
                arrowprops=dict(arrowstyle="<->", color="#CC0632", lw=2))

    plt.tight_layout()
    plt.savefig('assets/diagrama_conectividad_vial.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("diagrama_conectividad_vial.png generado con éxito")

# -----------------------------------------------------------------------------
# 2. ÁRBOL DE PROBLEMAS CAUSAL INSTITUCIONAL (CAPÍTULO 4)
# -----------------------------------------------------------------------------
def generar_arbol_problemas():
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # EFECTO FINAL (Arriba)
    box_ef_final = patches.FancyBboxPatch((1.5, 6.2), 8.0, 0.9, boxstyle="round,pad=0.15",
                                           facecolor="#FFF5F5", edgecolor="#CC0632", linewidth=2)
    ax.add_patch(box_ef_final)
    ax.text(5.5, 6.65, "EFECTO FINAL: Aislamiento territorial, alta vulnerabilidad climática y degradación socio-espacial",
            ha='center', va='center', fontsize=10, fontweight='bold', color='#900')

    # EFECTOS DIRECTOS
    efectos = [
        ("Efecto 1: Inseguridad vial y\nexclusión física de peatones", 1.8),
        ("Efecto 2: Inundaciones y erosión\nhídrica en laderas habitadas", 5.5),
        ("Efecto 3: Pérdida de calidad de\nvida y déficit de espacio público", 9.2)
    ]
    for texto, x in efectos:
        b = patches.FancyBboxPatch((x-1.5, 4.8), 3.0, 0.85, boxstyle="round,pad=0.1",
                                    facecolor="#FDFDFD", edgecolor="#CC0632", linewidth=1.2)
        ax.add_patch(b)
        ax.text(x, 5.22, texto, ha='center', va='center', fontsize=8.5, color='#333333', fontweight='semibold')
        # Flecha hacia arriba al efecto final
        ax.annotate('', xy=(5.5 if x == 5.5 else (3.5 if x < 5 else 7.5), 6.2), xytext=(x, 5.65),
                    arrowprops=dict(arrowstyle="->", color="#CC0632", lw=1.3))

    # PROBLEMA CENTRAL (Centro destacado)
    box_central = patches.FancyBboxPatch((0.8, 3.1), 9.4, 1.1, boxstyle="round,pad=0.15",
                                          facecolor="#CC0632", edgecolor="#8B0000", linewidth=2)
    ax.add_patch(box_central)
    ax.text(5.5, 3.8, "PROBLEMA CENTRAL", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#FFFFFF')
    ax.text(5.5, 3.4, "Deficiente conectividad vial, precariedad del espacio público y alta vulnerabilidad\nante amenazas hídricas en el Barrio El Capulí (Punzara)",
            ha='center', va='center', fontsize=9.2, color='#FFFFFF')

    # Flechas problema central -> efectos
    for _, x in efectos:
        ax.annotate('', xy=(x, 4.8), xytext=(x, 4.2),
                    arrowprops=dict(arrowstyle="->", color="#CC0632", lw=1.5))

    # CAUSAS DIRECTAS
    causas = [
        ("Causa Directa 1: Red vial de ladera\nsin obras de confinamiento ni veredas", 1.8),
        ("Causa Directa 2: Inexistencia de drenaje\nsostenible (SbN / SUDS)", 5.5),
        ("Causa Directa 3: Margen del río Capulí\ndesarticulado como botadero", 9.2)
    ]
    for texto, x in causas:
        b = patches.FancyBboxPatch((x-1.5, 1.7), 3.0, 0.85, boxstyle="round,pad=0.1",
                                    facecolor="#FDFDFD", edgecolor="#555555", linewidth=1.2)
        ax.add_patch(b)
        ax.text(x, 2.12, texto, ha='center', va='center', fontsize=8.5, color='#333333', fontweight='semibold')
        # Flecha hacia el problema central
        ax.annotate('', xy=(x, 3.1), xytext=(x, 2.55),
                    arrowprops=dict(arrowstyle="->", color="#555555", lw=1.5))

    # CAUSA RAÍZ (Abajo)
    box_raiz = patches.FancyBboxPatch((1.5, 0.3), 8.0, 0.85, boxstyle="round,pad=0.15",
                                       facecolor="#F6F6F6", edgecolor="#333333", linewidth=1.5)
    ax.add_patch(box_raiz)
    ax.text(5.5, 0.72, "Causa Raíz: Crecimiento periurbano no planificado en pendientes del 15% al 35%\nsin dotación reglamentaria de infraestructura vial ni drenaje pluvial",
            ha='center', va='center', fontsize=8.8, color='#222222', fontweight='bold')

    # Flechas causas directas <- causa raíz
    for _, x in causas:
        ax.annotate('', xy=(x, 1.7), xytext=(5.5 if x == 5.5 else (3.5 if x < 5 else 7.5), 1.15),
                    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2))

    plt.tight_layout()
    plt.savefig('assets/arbol_problemas_capuli.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("arbol_problemas_capuli.png generado con éxito")

# -----------------------------------------------------------------------------
# 3. ÁRBOL DE OBJETIVOS (MEDIOS - FINES) (CAPÍTULO 4)
# -----------------------------------------------------------------------------
def generar_arbol_objetivos():
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # FIN SUPERIOR (Arriba)
    box_fin = patches.FancyBboxPatch((1.5, 6.2), 8.0, 0.9, boxstyle="round,pad=0.15",
                                      facecolor="#F0F9F5", edgecolor="#1B6B42", linewidth=2)
    ax.add_patch(box_fin)
    ax.text(5.5, 6.65, "FIN SUPERIOR: Integración territorial sostenible, equidad socio-espacial y resiliencia climática",
            ha='center', va='center', fontsize=10, fontweight='bold', color='#1B6B42')

    # FINES DIRECTOS
    fines = [
        ("Fin 1: Movilidad activa segura,\ninclusiva y continua (8-80)", 1.8),
        ("Fin 2: Reducción del riesgo de\nescorrentía y taludes protegidos", 5.5),
        ("Fin 3: Espacio público verde ribereño\ny cohesión comunitaria", 9.2)
    ]
    for texto, x in fines:
        b = patches.FancyBboxPatch((x-1.5, 4.8), 3.0, 0.85, boxstyle="round,pad=0.1",
                                    facecolor="#FDFDFD", edgecolor="#1B6B42", linewidth=1.2)
        ax.add_patch(b)
        ax.text(x, 5.22, texto, ha='center', va='center', fontsize=8.5, color='#333333', fontweight='semibold')
        ax.annotate('', xy=(5.5 if x == 5.5 else (3.5 if x < 5 else 7.5), 6.2), xytext=(x, 5.65),
                    arrowprops=dict(arrowstyle="->", color="#1B6B42", lw=1.3))

    # PROPÓSITO / OBJETIVO GENERAL (Centro)
    box_central = patches.FancyBboxPatch((0.8, 3.1), 9.4, 1.1, boxstyle="round,pad=0.15",
                                          facecolor="#1B6B42", edgecolor="#0F472A", linewidth=2)
    ax.add_patch(box_central)
    ax.text(5.5, 3.8, "OBJETIVO GENERAL DEL PROYECTO", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#FFFFFF')
    ax.text(5.5, 3.4, "Implementar un sistema integral de conectividad activa, soluciones basadas en la naturaleza\ny consolidación del Parque Fluvial de río Capulí en la Parroquia Punzara",
            ha='center', va='center', fontsize=9.2, color='#FFFFFF')

    # Flechas objetivo general -> fines
    for _, x in fines:
        ax.annotate('', xy=(x, 4.8), xytext=(x, 4.2),
                    arrowprops=dict(arrowstyle="->", color="#1B6B42", lw=1.5))

    # COMPONENTES / MEDIOS
    medios = [
        ("Componente 1: Calle completa y\nsenderos peatonales de ladera", 1.8),
        ("Componente 2: Sistema de drenaje\nsostenible (cunetas verdes y SUDS)", 5.5),
        ("Componente 3: Parque Fluvial de río\nCapulí (Proyecto N° 11 SVU)", 9.2)
    ]
    for texto, x in medios:
        b = patches.FancyBboxPatch((x-1.5, 1.7), 3.0, 0.85, boxstyle="round,pad=0.1",
                                    facecolor="#FDFDFD", edgecolor="#005C8F", linewidth=1.2)
        ax.add_patch(b)
        ax.text(x, 2.12, texto, ha='center', va='center', fontsize=8.5, color='#333333', fontweight='semibold')
        ax.annotate('', xy=(x, 3.1), xytext=(x, 2.55),
                    arrowprops=dict(arrowstyle="->", color="#005C8F", lw=1.5))

    # ACCIONES OPERATIVAS BASE
    box_base = patches.FancyBboxPatch((1.5, 0.3), 8.0, 0.85, boxstyle="round,pad=0.15",
                                       facecolor="#F6F6F6", edgecolor="#333333", linewidth=1.5)
    ax.add_patch(box_base)
    ax.text(5.5, 0.72, "Medios de Base: Articulación interinstitucional UNL - GAD Loja, modelo financiero\nCAPEX/OPEX a 15 años y gobernanza comunitaria participativa",
            ha='center', va='center', fontsize=8.8, color='#222222', fontweight='bold')

    for _, x in medios:
        ax.annotate('', xy=(x, 1.7), xytext=(5.5 if x == 5.5 else (3.5 if x < 5 else 7.5), 1.15),
                    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2))

    plt.tight_layout()
    plt.savefig('assets/arbol_objetivos_capuli.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("arbol_objetivos_capuli.png generado con éxito")

if __name__ == '__main__':
    generar_diagrama_conectividad()
    generar_arbol_problemas()
    generar_arbol_objetivos()
