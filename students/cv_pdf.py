"""Génération automatique du CV étudiant en PDF avec ReportLab."""
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

MADAGASCAR_RED = colors.HexColor('#CE1126')
MADAGASCAR_GREEN = colors.HexColor('#007E33')
DARK_GRAY = colors.HexColor('#1F2937')


def generate_cv_pdf(student):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle('Name', parent=styles['Title'], textColor=MADAGASCAR_RED, fontSize=22, spaceAfter=2)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], textColor=DARK_GRAY, fontSize=11, spaceAfter=10)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], textColor=MADAGASCAR_GREEN, fontSize=13, spaceBefore=12, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)
    small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=colors.gray)

    elements = []
    elements.append(Paragraph(student.full_name, name_style))
    elements.append(Paragraph(f"{student.department} — {student.get_level_display()} — {student.university}", subtitle_style))

    contact_bits = []
    if student.user.email:
        contact_bits.append(student.user.email)
    if student.phone:
        contact_bits.append(student.phone)
    if student.city:
        contact_bits.append(student.city)
    if contact_bits:
        elements.append(Paragraph(" | ".join(contact_bits), small_style))

    elements.append(HRFlowable(width="100%", thickness=1.2, color=MADAGASCAR_RED, spaceBefore=8, spaceAfter=8))

    if student.bio:
        elements.append(Paragraph("Profil", section_style))
        elements.append(Paragraph(student.bio, body_style))

    skills = list(student.student_skills.select_related('skill').all())
    if skills:
        elements.append(Paragraph("Compétences", section_style))
        data = [["Compétence", "Catégorie", "Niveau"]]
        for s in skills:
            data.append([s.skill.name, s.skill.get_category_display(), s.get_level_display()])
        table = Table(data, colWidths=[60 * mm, 60 * mm, 40 * mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), MADAGASCAR_GREEN),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)

    projects = list(student.projects.all())
    if projects:
        elements.append(Paragraph("Projets", section_style))
        for p in projects:
            elements.append(Paragraph(f"<b>{p.title}</b> — {p.date.strftime('%m/%Y')}", body_style))
            elements.append(Paragraph(p.description, body_style))
            links = []
            if p.github_url:
                links.append(f"GitHub : {p.github_url}")
            if p.demo_url:
                links.append(f"Démo : {p.demo_url}")
            if p.technologies:
                links.append(f"Technologies : {p.technologies}")
            if links:
                elements.append(Paragraph(" • ".join(links), small_style))
            elements.append(Spacer(1, 6))

    certificates = list(student.certificates.all())
    if certificates:
        elements.append(Paragraph("Certificats", section_style))
        for c in certificates:
            elements.append(Paragraph(
                f"<b>{c.title}</b> — {c.organization} ({c.issue_date.strftime('%m/%Y')})", body_style
            ))

    experiences = list(student.experiences.all())
    if experiences:
        elements.append(Paragraph("Expériences", section_style))
        for e in experiences:
            period_end = "En cours" if e.is_current else (e.end_date.strftime('%m/%Y') if e.end_date else '')
            elements.append(Paragraph(
                f"<b>{e.title}</b> — {e.organization} ({e.start_date.strftime('%m/%Y')} - {period_end})", body_style
            ))
            if e.description:
                elements.append(Paragraph(e.description, body_style))
            elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 14))
    elements.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#E5E7EB')))
    elements.append(Paragraph("Généré automatiquement via SkillMap Madagascar", small_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer
