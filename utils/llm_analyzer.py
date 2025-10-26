import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
        
        if not self.api_key:
            raise ValueError("⚠️ Groq API key not found. Please set GROQ_API_KEY in your .env file")
            
        self.client = Groq(api_key=self.api_key)
    
    def analyze_resume_content(self, resume_text, job_description="", max_retries=2):
        """Analyze resume content using Groq LLM with retry mechanism"""
        
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    print(f"Retry attempt {attempt}/{max_retries}")
                
                return self._perform_analysis(resume_text, job_description)
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    print("All retry attempts failed, returning fallback analysis")
                    return self._get_fallback_analysis()
                continue
    
    def _perform_analysis(self, resume_text, job_description=""):
        """Perform the actual analysis"""
        try:
            # Truncate resume text if too long to avoid token limits
            max_resume_length = 3000
            if len(resume_text) > max_resume_length:
                resume_text = resume_text[:max_resume_length] + "..."
            
            prompt = f"""Analyze this resume and provide a JSON response with the exact structure shown below.

Resume: {resume_text}

Job Description: {job_description if job_description else "Not provided"}

Return ONLY valid JSON in this exact format:
{{
    "overall_score": 75,
    "ats_compatibility": {{
        "score": 80,
        "issues": ["Example issue"],
        "recommendations": ["Example recommendation"]
    }},
    "content_analysis": {{
        "score": 70,
        "strengths": ["Example strength"],
        "weaknesses": ["Example weakness"],
        "missing_sections": ["Example missing section"]
    }},
    "skills_analysis": {{
        "score": 85,
        "technical_skills": ["Python", "JavaScript"],
        "soft_skills": ["Communication", "Leadership"],
        "missing_skills": ["Example missing skill"],
        "skill_gaps": ["Example skill gap"]
    }},
    "experience_analysis": {{
        "score": 75,
        "years_of_experience": 3,
        "quantified_achievements": 2,
        "action_verbs_used": ["Developed", "Managed"],
        "improvement_suggestions": ["Example suggestion"]
    }},
    "formatting_analysis": {{
        "score": 80,
        "readability": 85,
        "structure": 75,
        "length_assessment": "appropriate",
        "formatting_issues": ["Example issue"]
    }},
    "keyword_optimization": {{
        "score": 70,
        "relevant_keywords": ["Example keyword"],
        "missing_keywords": ["Example missing keyword"],
        "keyword_density": "appropriate"
    }},
    "recommendations": {{
        "high_priority": ["Most important improvement"],
        "medium_priority": ["Moderate improvement"],
        "low_priority": ["Nice to have improvement"]
    }},
    "course_recommendations": [
        {{
            "skill": "Python",
            "courses": [
                {{
                    "title": "Python for Beginners",
                    "platform": "Coursera",
                    "level": "Beginner",
                    "reason": "Strengthen programming fundamentals"
                }}
            ]
        }}
    ]
}}"""

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ATS and resume analyst. Return ONLY valid JSON without any markdown formatting, code blocks, or additional text. Do not use ``` or any other formatting."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.2,
                max_tokens=3000
            )

            # Check if response is valid
            if not response or not response.choices:
                print("Error: Empty response from Groq API")
                return self._get_fallback_analysis()
            
            # Parse the JSON response
            analysis_text = response.choices[0].message.content
            
            if not analysis_text or analysis_text.strip() == "":
                print("Error: Empty content from Groq API")
                return self._get_fallback_analysis()
            
            analysis_text = analysis_text.strip()
            
            # Clean up the response if it has markdown formatting
            if analysis_text.startswith('```json'):
                analysis_text = analysis_text[7:]
            elif analysis_text.startswith('```'):
                analysis_text = analysis_text[3:]
            
            if analysis_text.endswith('```'):
                analysis_text = analysis_text[:-3]
            
            # Additional cleanup - remove any remaining backticks or whitespace
            analysis_text = analysis_text.strip().strip('`').strip()
            
            if not analysis_text:
                print("Error: No content after cleanup")
                return self._get_fallback_analysis()
            
            # Optional: Print first 100 chars of response for debugging
            # print(f"Debug: LLM response preview: {analysis_text[:100]}...")
            
            analysis = json.loads(analysis_text)
            
            # Validate the analysis structure
            if not isinstance(analysis, dict) or 'overall_score' not in analysis:
                print("Error: Invalid analysis structure from LLM")
                return self._get_fallback_analysis()
            
            return analysis

        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Raw response: {analysis_text[:200] if 'analysis_text' in locals() else 'No response'}")
            return self._get_fallback_analysis()
        except Exception as e:
            print(f"Error analyzing resume with LLM: {e}")
            return self._get_fallback_analysis()

    def generate_resume_suggestions(self, current_resume, target_role=""):
        """Generate specific suggestions for resume improvement"""
        try:
            prompt = f"""
            As a professional resume writer and career coach, provide specific, actionable suggestions to improve this resume for the target role: {target_role}

            Current Resume:
            {current_resume}

            Please provide suggestions in JSON format:
            {{
                "content_improvements": [
                    {{
                        "section": "section name",
                        "current": "current content or issue",
                        "suggested": "improved version",
                        "reason": "why this improvement helps"
                    }}
                ],
                "new_sections_to_add": [
                    {{
                        "section": "section name",
                        "content": "suggested content",
                        "importance": "high/medium/low"
                    }}
                ],
                "keyword_additions": [
                    {{
                        "keyword": "keyword to add",
                        "where": "where to add it",
                        "context": "how to naturally include it"
                    }}
                ],
                "formatting_improvements": [
                    "list of formatting suggestions"
                ]
            }}
            """

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume writer. Provide specific, actionable suggestions in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.4,
                max_tokens=2000
            )

            suggestions_text = response.choices[0].message.content.strip()
            
            # Clean up the response
            if suggestions_text.startswith('```json'):
                suggestions_text = suggestions_text[7:]
            if suggestions_text.endswith('```'):
                suggestions_text = suggestions_text[:-3]
            
            suggestions = json.loads(suggestions_text)
            return suggestions

        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return {
                "content_improvements": [],
                "new_sections_to_add": [],
                "keyword_additions": [],
                "formatting_improvements": []
            }

    def _get_fallback_analysis(self):
        """Fallback analysis when LLM fails - provides basic analysis"""
        return {
            "overall_score": 65,
            "ats_compatibility": {
                "score": 60,
                "issues": [
                    "Unable to perform AI analysis - using basic evaluation",
                    "Recommend manual review for ATS compatibility"
                ],
                "recommendations": [
                    "Use standard fonts and formatting",
                    "Include relevant keywords from job description",
                    "Avoid complex layouts and graphics"
                ]
            },
            "content_analysis": {
                "score": 65,
                "strengths": [
                    "Resume content detected and processed"
                ],
                "weaknesses": [
                    "Detailed AI analysis unavailable"
                ],
                "missing_sections": [
                    "Unable to determine - manual review needed"
                ]
            },
            "skills_analysis": {
                "score": 60,
                "technical_skills": ["Skills analysis unavailable"],
                "soft_skills": ["Manual review recommended"],
                "missing_skills": ["AI analysis required for skill gap identification"],
                "skill_gaps": ["Compare manually with job requirements"]
            },
            "experience_analysis": {
                "score": 60,
                "years_of_experience": 0,
                "quantified_achievements": 0,
                "action_verbs_used": ["Manual analysis needed"],
                "improvement_suggestions": [
                    "Use strong action verbs",
                    "Quantify achievements with numbers",
                    "Focus on results and impact"
                ]
            },
            "formatting_analysis": {
                "score": 70,
                "readability": 70,
                "structure": 70,
                "length_assessment": "unknown",
                "formatting_issues": ["AI analysis unavailable"]
            },
            "keyword_optimization": {
                "score": 60,
                "relevant_keywords": ["Manual keyword analysis needed"],
                "missing_keywords": ["Compare with job description manually"],
                "keyword_density": "unknown"
            },
            "recommendations": {
                "high_priority": [
                    "Configure Groq API key for full AI analysis",
                    "Ensure resume follows ATS-friendly formatting",
                    "Include relevant keywords from target job"
                ],
                "medium_priority": [
                    "Review resume sections for completeness",
                    "Quantify achievements where possible"
                ],
                "low_priority": [
                    "Consider professional resume review",
                    "Test with different ATS systems"
                ]
            },
            "course_recommendations": [
                {
                    "skill": "Resume Writing",
                    "courses": [
                        {
                            "title": "Resume Writing Fundamentals",
                            "platform": "Coursera",
                            "level": "Beginner",
                            "reason": "Learn ATS-friendly resume writing techniques"
                        }
                    ]
                }
            ]
        }

    def bulk_analyze_resumes(self, resume_texts):
        """Analyze multiple resumes for bulk processing"""
        results = []
        
        for i, resume_text in enumerate(resume_texts):
            print(f"Analyzing resume {i + 1} of {len(resume_texts)}")
            analysis = self.analyze_resume_content(resume_text)
            results.append({
                "resume_index": i + 1,
                "analysis": analysis
            })
        
        return results