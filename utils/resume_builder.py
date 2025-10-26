from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
from datetime import datetime

class ResumeBuilder:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for the resume"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2C3E50')
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12,
            textColor=colors.HexColor('#34495E'),
            borderWidth=1,
            borderColor=colors.HexColor('#BDC3C7'),
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
            textColor=colors.HexColor('#2980B9'),
            spaceBefore=6,
            spaceAfter=3
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=6
        ))

    def create_resume(self, data):
        """Create a professional resume PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Header section
        story.extend(self._create_header(data.get('personal_info', {})))
        
        # Summary section
        if data.get('summary'):
            story.extend(self._create_summary(data['summary']))
        
        # Experience section
        if data.get('experience'):
            story.extend(self._create_experience(data['experience']))
        
        # Education section
        if data.get('education'):
            story.extend(self._create_education(data['education']))
        
        # Skills section
        if data.get('skills'):
            story.extend(self._create_skills(data['skills']))
        
        # Projects section
        if data.get('projects'):
            story.extend(self._create_projects(data['projects']))
        
        # Certifications section
        if data.get('certifications'):
            story.extend(self._create_certifications(data['certifications']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _create_header(self, personal_info):
        """Create header with personal information"""
        story = []
        
        # Name
        name = personal_info.get('name', 'Your Name')
        story.append(Paragraph(name, self.styles['CustomHeader']))
        
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
        if personal_info.get('github'):
            contact_parts.append(f"GitHub: {personal_info['github']}")
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 12))
        return story

    def _create_summary(self, summary):
        """Create professional summary section"""
        story = []
        story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
        story.append(Paragraph(summary, self.styles['Normal']))
        story.append(Spacer(1, 12))
        return story

    def _create_experience(self, experiences):
        """Create work experience section"""
        story = []
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))
        
        for exp in experiences:
            # Job title and company
            job_title = exp.get('title', 'Job Title')
            company = exp.get('company', 'Company Name')
            location = exp.get('location', '')
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', 'Present')
            
            # Create job header table
            job_data = [
                [Paragraph(f"<b>{job_title}</b>", self.styles['JobTitle']),
                 Paragraph(f"{start_date} - {end_date}", self.styles['Normal'])]
            ]
            
            job_table = Table(job_data, colWidths=[4*inch, 2*inch])
            job_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(job_table)
            
            # Company and location
            company_text = company
            if location:
                company_text += f" | {location}"
            story.append(Paragraph(company_text, self.styles['Company']))
            
            # Responsibilities/achievements
            if exp.get('responsibilities'):
                for responsibility in exp['responsibilities']:
                    story.append(Paragraph(f"• {responsibility}", self.styles['Normal']))
            
            story.append(Spacer(1, 12))
        
        return story

    def _create_education(self, education_list):
        """Create education section"""
        story = []
        story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
        
        for edu in education_list:
            degree = edu.get('degree', 'Degree')
            school = edu.get('school', 'School Name')
            year = edu.get('year', '')
            gpa = edu.get('gpa', '')
            
            edu_text = f"<b>{degree}</b>"
            if year:
                edu_text += f" ({year})"
            story.append(Paragraph(edu_text, self.styles['Normal']))
            
            school_text = school
            if gpa:
                school_text += f" | GPA: {gpa}"
            story.append(Paragraph(school_text, self.styles['Company']))
            
            if edu.get('relevant_courses'):
                courses = ", ".join(edu['relevant_courses'])
                story.append(Paragraph(f"Relevant Courses: {courses}", self.styles['Normal']))
            
            story.append(Spacer(1, 6))
        
        return story

    def _create_skills(self, skills):
        """Create skills section"""
        story = []
        story.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
        
        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                if skill_list:
                    skills_text = ", ".join(skill_list)
                    story.append(Paragraph(f"<b>{category}:</b> {skills_text}", self.styles['Normal']))
        else:
            # If skills is a simple list
            skills_text = ", ".join(skills)
            story.append(Paragraph(skills_text, self.styles['Normal']))
        
        story.append(Spacer(1, 12))
        return story

    def _create_projects(self, projects):
        """Create projects section"""
        story = []
        story.append(Paragraph("PROJECTS", self.styles['SectionHeader']))
        
        for project in projects:
            title = project.get('title', 'Project Title')
            description = project.get('description', '')
            technologies = project.get('technologies', [])
            link = project.get('link', '')
            
            # Project title
            project_title = f"<b>{title}</b>"
            if link:
                project_title += f" | <link href='{link}'>{link}</link>"
            story.append(Paragraph(project_title, self.styles['Normal']))
            
            # Technologies
            if technologies:
                tech_text = f"Technologies: {', '.join(technologies)}"
                story.append(Paragraph(tech_text, self.styles['Company']))
            
            # Description
            if description:
                story.append(Paragraph(f"• {description}", self.styles['Normal']))
            
            story.append(Spacer(1, 6))
        
        return story

    def _create_certifications(self, certifications):
        """Create certifications section"""
        story = []
        story.append(Paragraph("CERTIFICATIONS", self.styles['SectionHeader']))
        
        for cert in certifications:
            name = cert.get('name', 'Certification Name')
            issuer = cert.get('issuer', 'Issuing Organization')
            date = cert.get('date', '')
            
            cert_text = f"<b>{name}</b> - {issuer}"
            if date:
                cert_text += f" ({date})"
            story.append(Paragraph(cert_text, self.styles['Normal']))
        
        story.append(Spacer(1, 12))
        return story

    def validate_section(self, section, content):
        """Validate resume section content"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        if section == 'personal_info':
            return self._validate_personal_info(content)
        elif section == 'summary':
            return self._validate_summary(content)
        elif section == 'experience':
            return self._validate_experience(content)
        elif section == 'education':
            return self._validate_education(content)
        elif section == 'skills':
            return self._validate_skills(content)
        
        return validation_result

    def _validate_personal_info(self, content):
        """Validate personal information"""
        result = {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': []}
        
        if not content.get('name'):
            result['errors'].append('Name is required')
            result['is_valid'] = False
        
        if not content.get('email'):
            result['errors'].append('Email is required')
            result['is_valid'] = False
        elif '@' not in content['email']:
            result['errors'].append('Invalid email format')
            result['is_valid'] = False
        
        if not content.get('phone'):
            result['warnings'].append('Phone number is recommended')
        
        if not content.get('location'):
            result['suggestions'].append('Consider adding your location')
        
        return result

    def _validate_summary(self, content):
        """Validate professional summary"""
        result = {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': []}
        
        if not content or len(content.strip()) < 50:
            result['warnings'].append('Summary should be at least 50 characters')
        
        if len(content) > 300:
            result['warnings'].append('Summary should be concise (under 300 characters)')
        
        # Check for action words
        action_words = ['achieved', 'developed', 'managed', 'led', 'created', 'improved']
        if not any(word in content.lower() for word in action_words):
            result['suggestions'].append('Consider using strong action words')
        
        return result

    def _validate_experience(self, experiences):
        """Validate work experience"""
        result = {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': []}
        
        if not experiences:
            result['warnings'].append('At least one work experience is recommended')
            return result
        
        for i, exp in enumerate(experiences):
            if not exp.get('title'):
                result['errors'].append(f'Job title is required for experience {i+1}')
                result['is_valid'] = False
            
            if not exp.get('company'):
                result['errors'].append(f'Company name is required for experience {i+1}')
                result['is_valid'] = False
            
            if not exp.get('responsibilities'):
                result['warnings'].append(f'Responsibilities are recommended for experience {i+1}')
            elif len(exp['responsibilities']) < 2:
                result['suggestions'].append(f'Consider adding more responsibilities for experience {i+1}')
        
        return result

    def _validate_education(self, education_list):
        """Validate education"""
        result = {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': []}
        
        if not education_list:
            result['warnings'].append('Education information is recommended')
            return result
        
        for i, edu in enumerate(education_list):
            if not edu.get('degree'):
                result['errors'].append(f'Degree is required for education {i+1}')
                result['is_valid'] = False
            
            if not edu.get('school'):
                result['errors'].append(f'School name is required for education {i+1}')
                result['is_valid'] = False
        
        return result

    def _validate_skills(self, skills):
        """Validate skills section"""
        result = {'is_valid': True, 'errors': [], 'warnings': [], 'suggestions': []}
        
        if not skills:
            result['warnings'].append('Skills section is highly recommended')
            return result
        
        if isinstance(skills, dict):
            total_skills = sum(len(skill_list) for skill_list in skills.values())
        else:
            total_skills = len(skills)
        
        if total_skills < 5:
            result['suggestions'].append('Consider adding more relevant skills')
        
        return result