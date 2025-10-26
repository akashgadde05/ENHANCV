from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import tempfile
import os
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for the resume"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='ResumeHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=3
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=6,
            spaceAfter=3,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))

    def generate_resume_pdf(self, resume_data):
        """Generate PDF resume from resume data"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_path = temp_file.name
            temp_file.close()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                temp_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Header section
            if resume_data.get('personal_info'):
                story.extend(self._build_header(resume_data['personal_info']))
            
            # Professional summary
            if resume_data.get('summary'):
                story.extend(self._build_summary(resume_data['summary']))
            
            # Experience section
            if resume_data.get('experience'):
                story.extend(self._build_experience(resume_data['experience']))
            
            # Education section
            if resume_data.get('education'):
                story.extend(self._build_education(resume_data['education']))
            
            # Skills section
            if resume_data.get('skills'):
                story.extend(self._build_skills(resume_data['skills']))
            
            # Projects section
            if resume_data.get('projects'):
                story.extend(self._build_projects(resume_data['projects']))
            
            # Certifications section
            if resume_data.get('certifications'):
                story.extend(self._build_certifications(resume_data['certifications']))
            
            # Build PDF
            doc.build(story)
            
            return temp_path
            
        except Exception as e:
            raise Exception(f"Error generating PDF: {str(e)}")

    def _build_header(self, personal_info):
        """Build header section with personal information"""
        story = []
        
        # Name
        if personal_info.get('name'):
            story.append(Paragraph(personal_info['name'], self.styles['ResumeHeader']))
        
        # Contact information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact_parts.append(f"LinkedIn: {personal_info['linkedin']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 12))
        return story

    def _build_summary(self, summary):
        """Build professional summary section"""
        story = []
        story.append(Paragraph("Professional Summary", self.styles['SectionHeader']))
        story.append(Paragraph(summary, self.styles['Normal']))
        story.append(Spacer(1, 12))
        return story

    def _build_experience(self, experience_list):
        """Build experience section"""
        story = []
        story.append(Paragraph("Professional Experience", self.styles['SectionHeader']))
        
        for exp in experience_list:
            # Job title and company
            title_company = f"<b>{exp.get('title', '')}</b>"
            if exp.get('company'):
                title_company += f" - {exp['company']}"
            story.append(Paragraph(title_company, self.styles['JobTitle']))
            
            # Duration and location
            duration_location = []
            if exp.get('duration'):
                duration_location.append(exp['duration'])
            if exp.get('location'):
                duration_location.append(exp['location'])
            
            if duration_location:
                story.append(Paragraph(" | ".join(duration_location), self.styles['Normal']))
            
            # Responsibilities/achievements
            if exp.get('responsibilities'):
                for resp in exp['responsibilities']:
                    story.append(Paragraph(f"• {resp}", self.styles['Normal']))
            
            story.append(Spacer(1, 8))
        
        return story

    def _build_education(self, education_list):
        """Build education section"""
        story = []
        story.append(Paragraph("Education", self.styles['SectionHeader']))
        
        for edu in education_list:
            # Degree and institution
            degree_school = f"<b>{edu.get('degree', '')}</b>"
            if edu.get('institution'):
                degree_school += f" - {edu['institution']}"
            story.append(Paragraph(degree_school, self.styles['Normal']))
            
            # Year and GPA
            details = []
            if edu.get('year'):
                details.append(edu['year'])
            if edu.get('gpa'):
                details.append(f"GPA: {edu['gpa']}")
            
            if details:
                story.append(Paragraph(" | ".join(details), self.styles['Normal']))
            
            story.append(Spacer(1, 6))
        
        return story

    def _build_skills(self, skills_data):
        """Build skills section"""
        story = []
        story.append(Paragraph("Skills", self.styles['SectionHeader']))
        
        if isinstance(skills_data, dict):
            for category, skills_list in skills_data.items():
                if skills_list:
                    skills_text = f"<b>{category}:</b> {', '.join(skills_list)}"
                    story.append(Paragraph(skills_text, self.styles['Normal']))
        elif isinstance(skills_data, list):
            skills_text = ", ".join(skills_data)
            story.append(Paragraph(skills_text, self.styles['Normal']))
        
        story.append(Spacer(1, 12))
        return story

    def _build_projects(self, projects_list):
        """Build projects section"""
        story = []
        story.append(Paragraph("Projects", self.styles['SectionHeader']))
        
        for project in projects_list:
            # Project name
            if project.get('name'):
                story.append(Paragraph(f"<b>{project['name']}</b>", self.styles['Normal']))
            
            # Description
            if project.get('description'):
                story.append(Paragraph(project['description'], self.styles['Normal']))
            
            # Technologies
            if project.get('technologies'):
                tech_text = f"<i>Technologies:</i> {', '.join(project['technologies'])}"
                story.append(Paragraph(tech_text, self.styles['Normal']))
            
            story.append(Spacer(1, 6))
        
        return story

    def _build_certifications(self, certifications_list):
        """Build certifications section"""
        story = []
        story.append(Paragraph("Certifications", self.styles['SectionHeader']))
        
        for cert in certifications_list:
            cert_text = cert.get('name', '')
            if cert.get('issuer'):
                cert_text += f" - {cert['issuer']}"
            if cert.get('year'):
                cert_text += f" ({cert['year']})"
            
            story.append(Paragraph(f"• {cert_text}", self.styles['Normal']))
        
        story.append(Spacer(1, 12))
        return story