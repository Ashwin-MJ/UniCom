from django.test import TestCase
from student_feedback_app import Student, Class, Lecturer, Feedback


class AddStudentTest(TestCase):
    def set_up(self):
        student = Student.objects.create(username="Eragon", student_slug="Eragon",
                               password="Saphira", email="Eragon@Alagaesia.com",
                               score=0, classes = NULL)
        student.save()
    def test_add_student(self):
        
