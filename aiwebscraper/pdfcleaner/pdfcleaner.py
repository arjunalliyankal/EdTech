from flask import Flask, render_template, request, jsonify, send_file
import re
import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

app = Flask(__name__)

class TextCleaner:
    def __init__(self):
        self.emoji_patterns = {
            '📘': '',
            '🔹': '• ',
            '📌': '• ',
            '🟦': '■ ',
            '🟨': '■ ',
            '⬜': '□ ',
            '➡️': '→ ',
            '✅': '✓ ',
            '📝': '',
            '🎯': '',
            '*': '',
        }
    
    def clean_text(self, text):
        """Clean and structure the input text"""
        # Remove excessive emojis and replace with appropriate symbols
        cleaned = text
        for emoji, replacement in self.emoji_patterns.items():
            cleaned = cleaned.replace(emoji, replacement)
        
        # Clean up markdown formatting
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cleaned)
        cleaned = re.sub(r'\*(.*?)\*', r'<em>\1</em>', cleaned)
        
        # Handle bullet points and lists
        cleaned = re.sub(r'^•\s*', '• ', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'^\*\s*', '• ', cleaned, flags=re.MULTILINE)
        
        # Clean up multiple spaces and newlines
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        
        # Structure sections
        sections = self.structure_sections(cleaned)
        return sections
    
    def structure_sections(self, text):
        """Structure text into logical sections with bullets, numbers, and headings"""
        lines = text.split('\n')
        structured_lines = []
        in_ul = False
        in_ol = False
        
        def close_lists():
            nonlocal in_ul, in_ol
            if in_ul:
                structured_lines.append('</ul>')
                in_ul = False
            if in_ol:
                structured_lines.append('</ol>')
                in_ol = False

        for line in lines:
            line = line.strip()
            if not line:
                close_lists()
                structured_lines.append('')
                continue

            # Heading detection (robust)
            if (line.startswith('• ') and any(keyword in line.lower() for keyword in ['what is', 'why use', 'types of', 'benefits', 'example'])) or re.match(r'^(#+) ', line):
                close_lists()
                # Markdown heading
                if re.match(r'^(#+) ', line):
                    hashes, title = re.match(r'^(#+) (.*)', line).groups()
                    level = min(len(hashes), 3)
                    structured_lines.append(f'<h{level}>{title}</h{level}>')
                else:
                    structured_lines.append(f'<h2>{line[2:]}</h2>')
            elif line.startswith('• ') and line.endswith(':'):
                close_lists()
                structured_lines.append(f'<h3>{line[2:-1]}</h3>')
            # Bullet point
            elif re.match(r'^(• |\*)', line):
                if not in_ul:
                    close_lists()
                    structured_lines.append('<ul>')
                    in_ul = True
                # Remove bullet char for <li>
                li_text = re.sub(r'^(• |\*)', '', line).strip()
                structured_lines.append(f'<li>{li_text}</li>')
            # Numbered list
            elif re.match(r'^[0-9]+\. ', line):
                if not in_ol:
                    close_lists()
                    structured_lines.append('<ol>')
                    in_ol = True
                li_text = re.sub(r'^[0-9]+\. ', '', line).strip()
                structured_lines.append(f'<li>{li_text}</li>')
            else:
                close_lists()
                structured_lines.append(f'<p>{line}</p>')
        close_lists()
        return '\n'.join(structured_lines)

def create_pdf(content, filename):
    """Create PDF from HTML content, supporting headings, paragraphs, and lists"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue,
        leftIndent=0
    )
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=10,
        textColor=colors.darkgreen,
        leftIndent=20
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leftIndent=0,
        alignment=TA_JUSTIFY
    )
    # Parse content and build story
    story = []
    story.append(Paragraph("Document Content", title_style))
    story.append(Spacer(1, 20))

    # List parsing state
    in_ul = False
    in_ol = False
    list_items = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            # Close any open lists
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
                in_ul = False
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
                in_ol = False
            story.append(Spacer(1, 6))
            continue
        if line.startswith('<h2>') and line.endswith('</h2>'):
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
                in_ul = False
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
                in_ol = False
            text = line[4:-5]
            story.append(Paragraph(text, heading_style))
        elif line.startswith('<h3>') and line.endswith('</h3>'):
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
                in_ul = False
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
                in_ol = False
            text = line[4:-5]
            story.append(Paragraph(text, subheading_style))
        elif line == '<ul>':
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
            in_ul = True
        elif line == '</ul>':
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
            in_ul = False
        elif line == '<ol>':
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
            in_ol = True
        elif line == '</ol>':
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
            in_ol = False
        elif line.startswith('<li>') and line.endswith('</li>'):
            text = line[4:-5]
            list_item = ListItem(Paragraph(text, normal_style))
            list_items.append(list_item)
        elif line.startswith('<p>') and line.endswith('</p>'):
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
                in_ul = False
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
                in_ol = False
            text = line[3:-4]
            story.append(Paragraph(text, normal_style))
        else:
            if in_ul and list_items:
                story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
                list_items = []
                in_ul = False
            if in_ol and list_items:
                story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
                list_items = []
                in_ol = False
            story.append(Paragraph(line, normal_style))
    # Close any open lists at the end
    if in_ul and list_items:
        story.append(ListFlowable(list_items, bulletType='bullet', leftIndent=20))
    if in_ol and list_items:
        story.append(ListFlowable(list_items, bulletType='1', leftIndent=20))
    doc.build(story)
    return temp_file.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clean', methods=['POST'])
def clean_text():
    """Clean and structure the input text"""
    data = request.get_json()
    input_text = data.get('text', '')
    
    cleaner = TextCleaner()
    cleaned_text = cleaner.clean_text(input_text)
    
    return jsonify({'cleaned_text': cleaned_text})

@app.route('/convert_to_pdf', methods=['POST'])
def convert_to_pdf():
    """Convert edited text to PDF"""
    data = request.get_json()
    content = data.get('content', '')
    
    # Create PDF
    pdf_file = create_pdf(content, 'document.pdf')
    
    # Return PDF file
    return send_file(pdf_file, as_attachment=True, download_name='cleaned_document.pdf', mimetype='application/pdf')





# Create templates directory and save HTML template
if not os.path.exists('templates'):
    os.makedirs('templates')

# with open('templates/index.html', 'w', encoding='utf-8') as f:
#     f.write(index.html)

if __name__ == '__main__':
    app.run(debug=True)