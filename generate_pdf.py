#!/usr/bin/env python3
"""Generate PDF from CHANGELOG.md using fpdf2 (fast, no external deps)"""
from fpdf import FPDF
import re

class ArabicPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(15, 52, 96)
        self.cell(0, 8, '0x7v11co - Security Scanner Changelog', align='C', new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def clean_text(text):
    """Remove markdown formatting for plain text"""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    return text.strip()

with open('/Users/mohadreamer/0x7v11co/CHANGELOG.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

pdf = ArabicPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

i = 0
in_code_block = False
code_buffer = []
in_table = False
table_rows = []

while i < len(lines):
    line = lines[i].rstrip()
    
    # Code blocks
    if line.startswith('```'):
        if in_code_block:
            # End code block
            pdf.set_font('Courier', '', 9)
            pdf.set_fill_color(26, 26, 46)
            pdf.set_text_color(0, 255, 65)
            code_text = '\n'.join(code_buffer)
            pdf.multi_cell(0, 4.5, code_text, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            code_buffer = []
            in_code_block = False
        else:
            in_code_block = True
        i += 1
        continue
    
    if in_code_block:
        code_buffer.append(line)
        i += 1
        continue
    
    # Tables
    if '|' in line and line.strip().startswith('|'):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if all(set(c) <= set('-: ') for c in cells):
            i += 1
            continue
        if not in_table:
            in_table = True
            # Header row
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_fill_color(15, 52, 96)
            pdf.set_text_color(255, 255, 255)
            col_w = (190) / max(len(cells), 1)
            for cell in cells:
                pdf.cell(col_w, 7, clean_text(cell), border=1, fill=True, align='C')
            pdf.ln()
            pdf.set_text_color(0, 0, 0)
        else:
            # Data row
            pdf.set_font('Helvetica', '', 8)
            pdf.set_fill_color(248, 249, 250)
            fill = (len(table_rows) % 2 == 0)
            for cell in cells:
                pdf.cell(col_w, 6, clean_text(cell), border=1, fill=fill, align='C')
            pdf.ln()
            table_rows.append(cells)
        i += 1
        continue
    elif in_table:
        in_table = False
        table_rows = []
        pdf.ln(3)
    
    # Empty lines
    if not line.strip():
        pdf.ln(2)
        i += 1
        continue
    
    # Horizontal rule
    if line.strip() == '---':
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_draw_color(200)
        pdf.dashed_line(10, y, 200, y, 2, 2)
        pdf.ln(4)
        i += 1
        continue
    
    # Headers
    if line.startswith('# '):
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 20)
        pdf.set_text_color(15, 52, 96)
        pdf.cell(0, 10, clean_text(line[2:]), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(233, 69, 96)
        pdf.set_line_width(0.8)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_line_width(0.2)
        pdf.ln(4)
        i += 1
        continue
    
    if line.startswith('## '):
        pdf.ln(4)
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(22, 33, 62)
        pdf.cell(0, 9, clean_text(line[3:]), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(15, 52, 96)
        pdf.line(10, pdf.get_y(), 120, pdf.get_y())
        pdf.ln(3)
        i += 1
        continue
    
    if line.startswith('### '):
        pdf.ln(3)
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(15, 52, 96)
        pdf.cell(0, 8, clean_text(line[4:]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        i += 1
        continue
    
    if line.startswith('#### '):
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(233, 69, 96)
        pdf.cell(0, 7, clean_text(line[5:]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        i += 1
        continue
    
    # Blockquote
    if line.startswith('> '):
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(100)
        pdf.set_fill_color(255, 243, 245)
        pdf.cell(3, 6, '', fill=False)
        pdf.set_x(pdf.get_x() + 2)
        pdf.multi_cell(0, 5, clean_text(line[2:]), fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        i += 1
        continue
    
    # List items
    if line.strip().startswith('- ') or line.strip().startswith('* '):
        indent = len(line) - len(line.lstrip())
        text = clean_text(line.strip()[2:])
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(26, 26, 46)
        pdf.cell(5 + indent * 3, 5, '')
        bullet = chr(8226) if indent == 0 else chr(9702)
        pdf.cell(5, 5, bullet)
        pdf.multi_cell(0, 5, text)
        i += 1
        continue
    
    # Regular text
    text = clean_text(line)
    if text:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(26, 26, 46)
        pdf.multi_cell(0, 5, text)
    
    i += 1

pdf.output('/Users/mohadreamer/0x7v11co/CHANGELOG.pdf')
print("PDF created: /Users/mohadreamer/0x7v11co/CHANGELOG.pdf")
