import docx
from docx.shared import Pt, RGBColor, Inches

doc_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\plantillas\custom_reference.docx"
doc = docx.Document(doc_path)

GIZ_RED = RGBColor(204, 6, 50)       # #CC0632
GIZ_DARK = RGBColor(51, 51, 51)     # #333333
GIZ_MUTED = RGBColor(102, 102, 102) # #666666

def set_font_and_color(style, font_name="Arial", size_pt=11, color=None, bold=False):
    font = style.font
    font.name = font_name
    font.size = Pt(size_pt)
    font.bold = bold
    if color:
        font.color.rgb = color

styles = doc.styles

# Normal (Body Text)
if 'Normal' in styles:
    s = styles['Normal']
    set_font_and_color(s, "Arial", 10.5, GIZ_DARK)
    s.paragraph_format.line_spacing = 1.15
    s.paragraph_format.space_after = Pt(4)
    s.paragraph_format.space_before = Pt(0)

# Title
if 'Title' in styles:
    s = styles['Title']
    set_font_and_color(s, "Arial", 22, GIZ_RED, bold=True)
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after = Pt(8)

# Subtitle
if 'Subtitle' in styles:
    s = styles['Subtitle']
    set_font_and_color(s, "Arial", 12, GIZ_DARK, bold=False)
    s.paragraph_format.space_after = Pt(14)

# Headings
heading_specs = {
    'Heading 1': (16, GIZ_RED, True, Pt(14), Pt(4)),
    'Heading 2': (13, GIZ_DARK, True, Pt(10), Pt(3)),
    'Heading 3': (11.5, GIZ_DARK, True, Pt(8), Pt(2)),
    'Heading 4': (10.5, GIZ_DARK, True, Pt(6), Pt(2)),
}

for name, (size, col, bold, sp_before, sp_after) in heading_specs.items():
    if name in styles:
        s = styles[name]
        set_font_and_color(s, "Arial", size, col, bold=bold)
        s.paragraph_format.space_before = sp_before
        s.paragraph_format.space_after = sp_after

# Blockquote
if 'Blockquote' in styles:
    s = styles['Blockquote']
    set_font_and_color(s, "Arial", 10, GIZ_DARK, bold=False)
    s.paragraph_format.left_indent = Inches(0.4)
    s.paragraph_format.right_indent = Inches(0.2)
    s.paragraph_format.space_before = Pt(4)
    s.paragraph_format.space_after = Pt(4)

out_path = r"d:\08_Ciclo\03_Practicas_Preprofesionales\docs\vaults\v04-expediente-proyecto-capuli\plantillas\giz_reference.docx"
doc.save(out_path)
print("Saved custom GIZ reference docx to:", out_path)
