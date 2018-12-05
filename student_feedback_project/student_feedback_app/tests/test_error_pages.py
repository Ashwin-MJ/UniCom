from django.test import Client
from django.test import TestCase

class StudentHomeErrorTestCase(TestCase):

    def set_up(self):
        authenticate(username='Ike', password='ikepass')
    
    def test_no_auth_page(self):
        c = Client()
        response = c.get('/student/home/')
        self.assertEqual(response.templates[0].name, "student_feedback_app/error_page.html")

    def test_no_auth_message(self):
        c = Client()
        response = c.get('/student/home/')
        self.assertContains(response, "You are not logged in")

    def test_exception_error_page(self):
        c = Client()
        print(c.login(username='Ike', password='ikepass'))
        response = c.get('/student/home/')
        #print(response.context)


#TODO figure out how to pass info to context dict or otherwise get error
#TODO get a user authenticated

