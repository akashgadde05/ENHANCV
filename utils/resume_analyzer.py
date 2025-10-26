import pypdf
import docx
import os
from textblob import TextBlob
import re
import pandas as pd
import numpy as np

class ResumeAnalyzer:
    def __init__(self):
        self.common_sections = [
            'summary', 'objective', 'experience', 'education', 'skills',
            'projects', 'certifications', 'achievements', 'awards'
        ]
        
        self.action_verbs = [
            'achieved', 'managed', 'led', 'developed', 'created', 'implemented',
            'improved', 'increased', 'reduced', 'optimized', 'designed',
            'built', 'launched', 'delivered', 'coordinated', 'supervised'
        ]

    def extract_text_from_file(self, file_path):
        """Extract text from PDF, DOCX, or TXT files"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_from_docx(file_path)
            elif file_extension == '.txt':
                return self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            raise Exception(f"Error extracting text from file: {str(e)}")

    def _extract_from_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        
        return text.strip()

    def _extract_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        
        return text.strip()

    def _extract_from_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
        
        return text.strip()

    def basic_analysis(self, text):
        """Perform basic text analysis without LLM"""
        analysis = {
            'word_count': len(text.split()),
            'character_count': len(text),
            'sections_found': self._find_sections(text),
            'contact_info': self._extract_contact_info(text),
            'skills_found': self._extract_basic_skills(text),
            'action_verbs_count': self._count_action_verbs(text),
            'quantified_achievements': self._find_quantified_achievements(text),
            'readability_score': self._calculate_readability(text)
        }
        
        return analysis

    def _find_sections(self, text):
        """Find common resume sections"""
        found_sections = []
        text_lower = text.lower()
        
        for section in self.common_sections:
            if section in text_lower:
                found_sections.append(section)
        
        return found_sections

    def _extract_contact_info(self, text):
        """Extract basic contact information"""
        contact_info = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone pattern
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
        
        return contact_info

    def _extract_basic_skills(self, text):
        """Extract basic skills using keyword matching"""
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node.js', 'sql', 'mongodb', 'aws', 'docker', 'kubernetes',
            'git', 'html', 'css', 'machine learning', 'data science'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in technical_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills

    def _count_action_verbs(self, text):
        """Count action verbs in the resume"""
        count = 0
        text_lower = text.lower()
        
        for verb in self.action_verbs:
            count += text_lower.count(verb)
        
        return count

    def _find_quantified_achievements(self, text):
        """Find quantified achievements (numbers, percentages, etc.)"""
        patterns = [
            r'\d+%',  # Percentages
            r'\$\d+',  # Dollar amounts
            r'\d+\+',  # Numbers with plus
            r'\d+k',   # Thousands
            r'\d+m',   # Millions
        ]
        
        achievements = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievements.extend(matches)
        
        return achievements

    def _calculate_readability(self, text):
        """Calculate basic readability score"""
        try:
            blob = TextBlob(text)
            sentences = len(blob.sentences)
            words = len(blob.words)
            
            if sentences == 0:
                return 0
            
            avg_sentence_length = words / sentences
            
            # Simple readability score (lower is better for resumes)
            if avg_sentence_length < 15:
                return 85
            elif avg_sentence_length < 20:
                return 70
            elif avg_sentence_length < 25:
                return 55
            else:
                return 40
                
        except Exception:
            return 50