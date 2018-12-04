from django.test import Client
from django.test import TestCase

class StudentHomeErrorTestCase(TestCase):
    
    def test_no_auth_page(self):
        c = Client()
        response = c.get('/student/home/')
        self.assertEqual(response.templates[0].name, "student_feedback_app/error_page.html")

    def test_no_auth_message(self):
        c = Client()
        response = c.get('/student/home/')
        self.assertContains(response, "You are not logged in")

