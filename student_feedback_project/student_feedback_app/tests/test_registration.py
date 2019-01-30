from django.test import TestCase

from student_feedback_app.models import User, LecturerProfile, StudentProfile
from student_feedback_app.forms import RegisterForm

class RegistrationTestCase(TestCase):

    def setUp(self):
        # Set up a few categories and pre defined messages
        user = User(id_number="101010",username="lecturer",is_lecturer=1,password="71gye7y1w21")
        user.save()
        user = User(id_number="010101",username="student",is_lecturer=0,password="71gye7y1w21")
        user.save()

    def test_lecturer_creation(self):
        user = User.objects.get(id_number="101010")
        self.assertTrue(LecturerProfile.objects.get(lecturer=user))

    def test_student_creation(self):
        user = User.objects.get(id_number="010101")
        self.assertTrue(StudentProfile.objects.get(student=user))
    
    def test_verification(self):
        user = User.objects.get(id_number="101010")
        self.assertEqual(user.is_active, 0)
