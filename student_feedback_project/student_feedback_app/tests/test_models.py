from student_feedback_app.models import Course
from django.test import TestCase
from populate.py import *

class StudentTestCase(TestCase):
    def setUp(self):
        add_class("Systems Programming 3", "SP3", "Introduction to Systems Programming using C and C++")
        add_student("Bob", "3015244", "Bob", "Bob@bob.bob", 0, "SP3")

    def test_student_in_course(self):
        course = Class.objects.get(course_code = "SP3")
        student = StudentProfile.objects.get(student.student_id = "3015244")
        self.assertEqual(course.students, student)

    def test_course_in_student(self):
        course = Class.objects.get(course_code = "SP3")
        student = StudentProfile.objects.get(student.student_id = "3015244")
        self.assertEqual(student.classes, course)


class CourseTestCase(TestCase):

    # Add test cases here e.g:
    def setUp(self):
        course = Course(subject="Systems Programming 3",
                        course_description="Introduction to Systems Programming using C and C++",
                        course_code="SP3")
        course.save()

    # Ensure all test methods begin with test_..... otherwise they will not run
    def test_course_slug_correct(self):
        # The slug for the above course should be sp3
        systems = Course.objects.get(course_code="SP3")
        self.assertEqual(systems.subject_slug, "sp3")

    def test_course_description_correct(self):
        systems = Course.objects.get(course_code="SP3")
        self.assertEqual(systems.course_description, "Introduction to Systems Programming using C and C++")

class FeedbackTestCase(TestCase):
    def setUp(self):
    def test_date_given_is_now(self):
