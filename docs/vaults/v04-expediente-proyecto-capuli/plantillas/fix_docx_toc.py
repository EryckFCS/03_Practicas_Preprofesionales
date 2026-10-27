import os
import docx
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_apa_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def set_row_bottom_border(row, sz="6"):
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="000000"/>
            </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

def process_word_document(file_path):
    doc = docx.Document(file_path)
    
    # 1. Habilitar w:updateFields para actualización en Word
    settings = doc.settings._element
    update_fields = parse_xml(r'<w:updateFields %s w:val="true"/>' % nsdecls('w'))
    settings.append(update_fields)

    # 2. Localizar todos los encabezados y asegurar bookmarks únicos para cada uno
    # También recopilar la información para la TOC
    heading_entries = [] # lista de (level, text, bookmark_name)
    bookmark_id_counter = 1000

    for i, p in enumerate(doc.paragraphs):
        s_name = p.style.name
        if s_name in ['Heading 1', 'Heading 2', 'Heading 3']:
            level = 1 if s_name == 'Heading 1' else (2 if s_name == 'Heading 2' else 3)
            text = p.text.strip()
            if not text:
                continue

            # Buscar bookmark previo o dentro de p
            bm_name = None
            for bm in p._element.findall(f'.//{qn("w:bookmarkStart")}'):
                name = bm.get(qn("w:name"))
                if name and not name.startswith('_'):
                    bm_name = name
                    break
            
            if not bm_name:
                prev = p._element.getprevious()
                if prev is not None and prev.tag.endswith('bookmarkStart'):
                    name = prev.get(qn("w:name"))
                    if name and not name.startswith('_'):
                        bm_name = name

            if not bm_name:
                bookmark_id_counter += 1
                bm_name = f"toc_bm_{bookmark_id_counter}"
                bm_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id_counter}" w:name="{bm_name}"/>')
                bm_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id_counter}"/>')
                p._element.insert(0, bm_start)
                p._element.append(bm_end)

            heading_entries.append((level, text, bm_name))

    print(f"Total headings registered with bookmarks: {len(heading_entries)}")

    # 3. Construir la Tabla de Contenidos (TOC) limpia y con hipervínculos funcionales
    body = doc._body._element
    sdt_elements = body.xpath('.//w:sdt')
    if sdt_elements:
        sdt = sdt_elements[0]
        sdtContent = sdt.find(qn('w:sdtContent'))
        if sdtContent is not None:
            # Vaciar todo el contenido previo de sdtContent para evitar duplicaciones
            for child in list(sdtContent):
                sdtContent.remove(child)

            # Título del Índice (Centrado, Times New Roman, Negrita)
            title_p = parse_xml(f'''
            <w:p {nsdecls("w")}>
                <w:pPr>
                    <w:pStyle w:val="TOCHeading"/>
                    <w:jc w:val="center"/>
                    <w:spacing w:before="120" w:after="240"/>
                </w:pPr>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
                        <w:b/>
                        <w:sz w:val="24"/>
                        <w:szCs w:val="24"/>
                        <w:color w:val="000000"/>
                    </w:rPr>
                    <w:t>Índice de Contenido</w:t>
                </w:r>
            </w:p>
            ''')
            sdtContent.append(title_p)

            # Campo dinámico nativo de Word para actualización
            field_p = parse_xml(f'''
            <w:p {nsdecls("w")}>
                <w:r>
                    <w:fldChar w:fldCharType="begin" w:dirty="true"/>
                    <w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>
                    <w:fldChar w:fldCharType="separate"/>
                    <w:fldChar w:fldCharType="end"/>
                </w:r>
            </w:p>
            ''')
            sdtContent.append(field_p)

            # Renderizado visual de cada línea con hipervínculo interno (<w:hyperlink w:anchor="...">)
            for level, text, bm_name in heading_entries:
                left_indent = 0 if level == 1 else (360 if level == 2 else 720) # 0, 0.25", 0.5"
                is_bold = "true" if level == 1 else "false"

                line_xml = f'''
                <w:p {nsdecls("w")}>
                    <w:pPr>
                        <w:pStyle w:val="TOC{level}"/>
                        <w:ind w:left="{left_indent}"/>
                        <w:tabs>
                            <w:tab w:val="right" w:leader="dot" w:pos="9360"/>
                        </w:tabs>
                        <w:spacing w:before="40" w:after="40" w:line="280" w:lineRule="auto"/>
                    </w:pPr>
                    <w:hyperlink w:anchor="{bm_name}">
                        <w:r>
                            <w:rPr>
                                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
                                <w:b w:val="{is_bold}"/>
                                <w:sz w:val="22"/>
                                <w:szCs w:val="22"/>
                                <w:color w:val="000000"/>
                            </w:rPr>
                            <w:t>{text}</w:t>
                        </w:r>
                        <w:r>
                            <w:rPr>
                                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
                                <w:sz w:val="22"/>
                            </w:rPr>
                            <w:tab/>
                        </w:r>
                        <w:r>
                            <w:rPr>
                                <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
                                <w:sz w:val="22"/>
                                <w:color w:val="333333"/>
                            </w:rPr>
                            <w:t>#</w:t>
                        </w:r>
                    </w:hyperlink>
                </w:p>
                '''
                sdtContent.append(parse_xml(line_xml))

            # Salto de página formal tras la TOC
            pb_p = parse_xml(f'''
            <w:p {nsdecls("w")}>
                <w:r>
                    <w:br w:type="page"/>
                </w:r>
            </w:p>
            ''')
            sdtContent.append(pb_p)

    # 4. Formatear y justificar párrafos del documento (Times New Roman 12pt, Justificado)
    in_ref_section = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        s_name = p.style.name

        # Detección de sección de referencias
        if s_name.startswith('Heading') and 'referencia' in txt.lower():
            in_ref_section = True
            continue
        elif s_name.startswith('Heading') and in_ref_section:
            in_ref_section = False

        # Si es la sección de referencias: Sangría francesa, 12pt, justificado/izquierda
        if in_ref_section and txt:
            pPr = p._p.get_or_add_pPr()
            numPr = pPr.find(qn('w:numPr'))
            if numPr is not None:
                pPr.remove(numPr)
            
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.first_line_indent = Inches(-0.5)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)

            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0, 0, 0)
            continue

        # Si son párrafos regulares de texto (First Paragraph, Body Text, Normal fuera de títulos)
        if s_name in ['Normal', 'Body Text', 'First Paragraph']:
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.first_line_indent = Inches(0.5)

            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0, 0, 0)

        elif s_name.startswith('Heading'):
            # Los encabezados no llevan sangría de primera línea
            p.paragraph_format.first_line_indent = Inches(0)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.color.rgb = RGBColor(0, 0, 0)

    # 5. Formateo de Tablas APA 7:
    # - Texto a 10 puntos (Pt(10)), Times New Roman, interlineado sencillo (1.15)
    # - Bordes superior, inferior y cabecera (sin líneas verticales)
    all_tables = list(doc.tables)
    tables_to_format = []
    for t in all_tables:
        tables_to_format.append(t)
        for row in t.rows:
            for cell in row.cells:
                for nested in cell.tables:
                    tables_to_format.append(nested)

    for t in tables_to_format:
        set_apa_table_borders(t)
        if len(t.rows) > 0:
            set_row_bottom_border(t.rows[0], sz="6")

        for r_idx, row in enumerate(t.rows):
            for cell in row.cells:
                set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                for p in cell.paragraphs:
                    p.paragraph_format.first_line_indent = Inches(0)
                    p.paragraph_format.left_indent = Inches(0)
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(1)
                    
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10) # 10 puntos en tablas
                        r.font.color.rgb = RGBColor(0, 0, 0)
                        if r_idx == 0:
                            r.font.bold = True

    doc.save(file_path)
    print(f"Successfully processed document: {file_path}")

if __name__ == "__main__":
    target = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\plantillas\plantilla_metodologia_giz_apa.docx"
    process_word_document(target)
