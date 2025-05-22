import json

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, HRFlowable, Table, \
    TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

def create_resume(json_file):
    data = json.load(open(json_file))

    create_resume_from_json(f"{data["header"]["name"].replace(" ", "_")}.pdf", data)

# Custom styles
header_style = ParagraphStyle(name='Header', fontSize=16, alignment=TA_CENTER, spaceAfter=6, spaceBefore=3, leading=20, fontName='Times-Bold')
contact_style = ParagraphStyle(name='Contact', fontSize=10, alignment=TA_CENTER, spaceAfter=15, fontName='Times-Roman')
section_title = ParagraphStyle(name='SectionTitle', fontSize=12, spaceBefore=10, spaceAfter=6, fontName='Times-Bold')
subheader = ParagraphStyle(name='Subheader', fontSize=11, fontName='Times-Bold', spaceAfter=2)
italic = ParagraphStyle(name='Italic', fontSize=10, fontName='Times-Italic')
normal = ParagraphStyle(name='Normal', fontSize=10, fontName='Times-Roman')

SPACER = Spacer(1, 10)
SMALL_SPACER = Spacer(1, 5)
LINE = HRFlowable(width='100%', thickness=0.5, color=colors.black)

def create_resume_from_json(pdf_path, data):
    doc = SimpleDocTemplate(pdf_path, pagesize=LETTER,
                            rightMargin=12, leftMargin=12,
                            topMargin=24, bottomMargin=24)

    content = []

    #Header
    content.append(Paragraph(data['header']['name'], header_style))
    description = f"{data['header']['email']} • {data['header']['phone']} • {data['header']['address']}"
    content.append(Paragraph(description, contact_style))

    doc.canv.setTitle(f'{data['header']['name']}\'s Resume')

    # EDUCATION
    education_data = data['education']

    if education_data:
        create_education(content, education_data)

    # PROFESSIONAL EXPERIENCE
    experience_data = data['experience']

    if experience_data:
        create_experience(content, experience_data)

    # LEADERSHIP AND INVOLVEMENT
    leadership_data = data['leadership']

    if leadership_data:
        create_leadership(content, leadership_data)

    # INTERESTS
    interests = data['interests']

    if interests:
        create_interests(content, interests)

    doc.build(content)
    print(f"Resume generated: {pdf_path}")

def create_education(content, education_data):
    content.append(Paragraph("EDUCATION", section_title))
    content.append(LINE)
    for element in education_data:
        content.append(lr_block(
            element['school'],
            element['major'],
            element['location'],
            element['date'],
            subheader,
            italic,
            subheader,
            italic
        ))

        content.append(Paragraph(f'{bold('Minors:')} {', '.join(element['minors'])}', normal))
        content.append(Paragraph(f'{bold('GPA:')} {element['gpa']}', normal))
        if (element['technical_skills']):
            content.append(Paragraph(f'{bold('Technical Skills:')} {', '.join(element['technical_skills'])}', normal))

        if (element['relevant_coursework']):
            content.append(Paragraph(f'{bold('Relevant Coursework:')} {', '.join(element['relevant_coursework'])}', normal))

def create_experience(content, experience_data):
    content.append(SPACER)
    content.append(Paragraph("PROFESSIONAL EXPERIENCE", section_title))
    content.append(LINE)

    i = 0

    for element in experience_data:
        if i != 0:
            content.append(SMALL_SPACER)

        content.append(lr_block(
            element['company'],
            element['title'],
            element['location'],
            element['date'],
            subheader,
            italic,
            subheader,
            italic
        ))

        if element['details']:
            items = []
            for detail in element['details']:
                items.append(ListItem(Paragraph(detail, normal)))

            content.append(ListFlowable(
                items, bulletType='bullet'
            ))

        i += 1

def create_leadership(content, leadership_data):

    content.append(Paragraph("LEADERSHIP AND INVOLVEMENT", section_title))
    content.append(LINE)

    i = 0

    for element in leadership_data:
        if i != 0:
            content.append(SMALL_SPACER)

        content.append(lr_block(
            element['organization'],
            element['role'],
            element['location'],
            element['date'],
            subheader,
            italic,
            subheader,
            italic
        ))

        if element['details']:
            items = []
            for detail in element['details']:
                items.append(ListItem(Paragraph(detail, normal)))

            content.append(ListFlowable(
                items, bulletType='bullet'
            ))

        i += 1

def create_interests(content, interests):
    content.append(Paragraph("INTERESTS", section_title))
    content.append(LINE)
    content.append(SMALL_SPACER)

    content.append(Paragraph(', '.join(interests), normal))

def bold(inline):
    return f'<b>{inline}</b>'

def lr_block(company, title, location, date,
                  company_style, title_style, location_style, date_style):
    # Just a list, no KeepTogether
    left = [Paragraph(company, company_style), Paragraph(title, title_style)]
    right = [Paragraph(location, location_style), Paragraph(date, date_style)]

    data = [[left, right]]
    table = Table(data, colWidths=["75%", "25%"])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table
