import docx
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\plantillas\custom_reference.docx"
doc = docx.Document(doc_path)

COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_MUTED = RGBColor(51, 51, 51)

def format_style(style, font_name="Times New Roman", size_pt=12, color=COLOR_BLACK, bold=False, italic=False):
    font = style.font
    font.name = font_name
    font.size = Pt(size_pt)
    font.bold = bold
    font.italic = italic
    font.color.rgb = color

styles = doc.styles

# 1. Normal (Texto base: Times New Roman 12pt, interlineado 1.5, primera línea 0.5")
if 'Normal' in styles:
    s = styles['Normal']
    format_style(s, "Times New Roman", 12, COLOR_BLACK)
    s.paragraph_format.line_spacing = 1.5
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.first_line_indent = Inches(0.5)

# 2. Body Text (Párrafos normales subsiguientes generados por Pandoc)
if 'Body Text' in styles:
    s = styles['Body Text']
    format_style(s, "Times New Roman", 12, COLOR_BLACK)
    s.paragraph_format.line_spacing = 1.5
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.first_line_indent = Inches(0.5)

# 3. First Paragraph (Primer párrafo tras títulos: según APA 7 en rigor los párrafos llevan sangría 0.5")
if 'First Paragraph' in styles:
    s = styles['First Paragraph']
    format_style(s, "Times New Roman", 12, COLOR_BLACK)
    s.paragraph_format.line_spacing = 1.5
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after = Pt(0)
    s.paragraph_format.first_line_indent = Inches(0.5)

# 4. Title & Subtitle
if 'Title' in styles:
    s = styles['Title']
    format_style(s, "Times New Roman", 14, COLOR_BLACK, bold=True)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.space_before = Pt(12)
    s.paragraph_format.space_after = Pt(6)

if 'Subtitle' in styles:
    s = styles['Subtitle']
    format_style(s, "Times New Roman", 12, COLOR_MUTED, bold=False, italic=True)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.space_after = Pt(18)

# 5. Headings APA 7
if 'Heading 1' in styles:
    s = styles['Heading 1']
    format_style(s, "Times New Roman", 12, COLOR_BLACK, bold=True)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.space_before = Pt(14)
    s.paragraph_format.space_after = Pt(6)

if 'Heading 2' in styles:
    s = styles['Heading 2']
    format_style(s, "Times New Roman", 12, COLOR_BLACK, bold=True)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.space_before = Pt(12)
    s.paragraph_format.space_after = Pt(4)

if 'Heading 3' in styles:
    s = styles['Heading 3']
    format_style(s, "Times New Roman", 12, COLOR_BLACK, bold=True, italic=True)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.space_before = Pt(10)
    s.paragraph_format.space_after = Pt(4)

if 'Heading 4' in styles:
    s = styles['Heading 4']
    format_style(s, "Times New Roman", 12, COLOR_BLACK, bold=True)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    s.paragraph_format.first_line_indent = Inches(0.5)
    s.paragraph_format.space_before = Pt(8)
    s.paragraph_format.space_after = Pt(2)

# 6. Blockquote
if 'Blockquote' in styles:
    s = styles['Blockquote']
    format_style(s, "Times New Roman", 11, COLOR_BLACK)
    s.paragraph_format.left_indent = Inches(0.5)
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.line_spacing = 1.5
    s.paragraph_format.space_before = Pt(6)
    s.paragraph_format.space_after = Pt(6)

# 7. Bibliography / Referencias APA 7:
# Sangría francesa (Hanging indent) de 0.5", interlineado 1.5, sin viñetas
if 'Bibliography' in styles:
    s = styles['Bibliography']
    format_style(s, "Times New Roman", 12, COLOR_BLACK)
    s.paragraph_format.left_indent = Inches(0.5)
    s.paragraph_format.first_line_indent = Inches(-0.5) # Sangría francesa
    s.paragraph_format.line_spacing = 1.5
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after = Pt(6)

# 8. Table Caption
if 'Table Caption' in styles:
    s = styles['Table Caption']
    format_style(s, "Times New Roman", 11, COLOR_BLACK, italic=True)
    s.paragraph_format.first_line_indent = Inches(0)
    s.paragraph_format.space_before = Pt(6)
    s.paragraph_format.space_after = Pt(2)

out_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\plantillas\giz_apa_reference.docx"
doc.save(out_path)
print("Saved updated APA 7 reference docx to:", out_path)
