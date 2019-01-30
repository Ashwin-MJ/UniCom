from django.test import TestCase
from student_feedback_app.models import User
from django.contrib.auth import SESSION_KEY
from django.test import Client
from populate import *


class LoginTestCase(TestCase):

    def setUp(self):
        # Set up a few categories and pre defined messages
        add_lecturer("name", "001", "password", "e@ma.il", [])
        add_student("name1", "0011", "e1@ma.il", "password", 0, [])

    def test_login(self):
        c = Client()
        c.login(id_number = "001", password = "password")
        response = c.get('/lecturer/home/', follow=True)
        self.assertContains(response, "Home Page")
        
    def test_restrictions_as_visitor(self):
        c = Client()
        response = c.get('/', follow=True)
        self.assertContains(response, "Log in")
        
    
    def test_restrictions_as_lecturer(self):
        c = Client()
        c.login(id_number = "001", password = "password")
        response = c.get('/student/home/', follow=True)
        self.assertContains(response, "Error")
        response = c.get('/lecturer/home/', follow=True)
        self.assertContains(response, "Home Page")
        
        
    def test_restrictions_as_student(self):
        c = Client()
        c.login(id_number = "0011", password = "password")
        response = c.get('/lecturer/courses/', follow=True)
        self.assertContains(response, "Error")
        response = c.get('/student/home/', follow=True)
        self.assertContains(response, "Home Page")
        
    

