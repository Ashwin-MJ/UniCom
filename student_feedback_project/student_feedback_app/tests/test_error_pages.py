from django.test import Client
from django.test import TestCase
from populate import *

class StudentHomeErrorTestCase(TestCase):

    def setUp(self):
        add_course("Systems Programming 3", "SP3", "Introduction to Systems Programming using C and C++")
        add_student("Bob", "3015244", "Bob@bob.bob", "Bob", 0, ["SP3"])
        add_lecturer("Wolf", "00001", "star", "wolf@star.com", ["SP3"])

    def test_no_auth_page(self):
        c = Client()
        response = c.get('/student/home/')
        self.assertEqual(response.templates[0].name, "student_feedback_app/error_page.html")

    def test_no_auth_message(self):
        c = Client()
        response = c.get('/student/home/')
        self.assertContains(response, "You Are Not Logged In")

    def test_lecturer_wrong_auth_page(self):
        c = Client()
        c.login(username="00001", password="wrong")
        response = c.get('/student/home/')
        self.assertEqual(response.templates[0].name, "student_feedback_app/error_page.html")
        c.logout()

    def test_exception_error_page(self):
        c = Client()
        c.login(username="3015244", password="Bob")
        response = c.get('/student/home/')
        c.logout()
        #print(response.content)
        #print(response.context)


#TODO figure out how to pass info to context dict or otherwise get error
