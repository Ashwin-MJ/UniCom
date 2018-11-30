from student_feedback_app.models import Course
from django.test import TestCase

class CourseTestCase(TestCase):

    # Add test cases here e.g:
    def setUp(self):
        course = Course(subject="Systems Programming 3",
                        course_description="Introduction to Systems Programming using C and C++",
                        course_code="SP3",)
        course.save()

    # Ensure all test methods begin with test_..... otherwise they will not run
    def test_course_token_correct_format(self):
        # The slug for the above course should be sp3


        systems = Course.objects.get(course_code="SP3")
        self.assertEqual(len(systems.course_token), 7)


    def test_create_course_that_exists(self):
        flag = False
        try:
            new_course = Course(course_code = 'SP3',)
            course.save()

        except:
            flag = True

        self.assertEqual(flag, True)