from student_feedback_app.models import Course
from django.test import TestCase

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
