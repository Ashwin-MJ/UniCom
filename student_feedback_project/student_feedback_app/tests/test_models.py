from student_feedback_app.models import *
from django.test import TestCase
from populate import *

class StudentTestCase(TestCase):
    def setUp(self):
        add_course("Systems Programming 3", "SP3", "Introduction to Systems Programming using C and C++")
        add_student("Bob", "3015244", "Bob@bob.bob", "Bob", 0, ["SP3"])

    def test_student_in_course(self):
        course = Course.objects.get(course_code = "SP3")
        testUser = User.objects.get(username = "Bob")
        testStudent = StudentProfile.objects.get(student=testUser)
        self.assertTrue(testStudent in course.students.all())

    def test_course_in_student(self):
        course = Course.objects.get(course_code = "SP3")
        testUser = User.objects.get(username = "Bob")
        testStudent = StudentProfile.objects.get(student=testUser)
        self.assertTrue(course in testStudent.courses.all())


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
        
    # Ensure entered course code matches course code in database
    def test_course_description_correct(self):
        systems = Course.objects.get(course_code="SP3")
        self.assertEqual(systems.course_description, "Introduction to Systems Programming using C and C++")

#class FeedbackTestCase(TestCase):
  #  def setUp(self):
   #    add_feedback(1, "writing", 4, "00001", 
    #def test_date_given_is_now(self):
