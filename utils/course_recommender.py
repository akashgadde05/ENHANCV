import json
from collections import defaultdict

class CourseRecommender:
    def __init__(self):
        # Course database with recommendations from multiple platforms
        self.course_database = {
            'python': [
                {
                    'title': 'Python for Everybody Specialization',
                    'platform': 'Coursera',
                    'provider': 'University of Michigan',
                    'level': 'Beginner',
                    'duration': '8 months',
                    'rating': 4.8,
                    'url': 'https://www.coursera.org/specializations/python'
                },
                {
                    'title': 'Complete Python Bootcamp',
                    'platform': 'Udemy',
                    'provider': 'Jose Portilla',
                    'level': 'Beginner to Advanced',
                    'duration': '22 hours',
                    'rating': 4.6,
                    'url': 'https://www.udemy.com/course/complete-python-bootcamp/'
                }
            ],
            'javascript': [
                {
                    'title': 'JavaScript Algorithms and Data Structures',
           