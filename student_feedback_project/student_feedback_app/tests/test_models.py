from student_feedback_app.models import *
from django.test import TestCase
from populate import *

# Ensure all test methods begin with test_..... otherwise they will not run

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

    def setUp(self):
        add_course("Systems Programming 3", "SP3", "Introduction to Systems Programming using C and C++")

    def test_course_slug_correct(self):
        # The slug for the above course should be sp3
        systems = Course.objects.get(course_code="SP3")
        self.assertEqual(systems.subject_slug, "sp3")
        
    def test_course_description_correct(self):
        systems = Course.objects.get(course_code="SP3")
        self.assertEqual(systems.course_description, "Introduction to Systems Programming using C and C++")

class FeedbackTestCase(TestCase):
    
    def setUp(self):
        add_course("Systems Programming 3", "SP3", "Introduction to Systems Programming using C and C++")
        add_lecturer("Wolf", "00001", "star", "wolf@star.com", ["SP3"])
        add_student("Bob", "3015244", "Bob@bob.bob", "Bob", 0, ["SP3"])
        add_category("writing")
        add_message("writing", "wrote well")
        add_feedback(1, "writing", 4, "00001", "3015244", "SP3", "wrote well", "good explanation of pointers") 
                    
    def test_fb_correct_optional_message(self):
        fb = Feedback.objects.get(feedback_id=1)
        self.assertEqual(fb.optional_message, "good explanation of pointers")

    def test_fb_correct_lecturer(self):
        fb = Feedback.objects.get(feedback_id=1)
        self.assertEqual(fb.lecturer.lecturer.username, "Wolf")

    def test_fb_correct_student(self):
        fb = Feedback.objects.get(feedback_id=1)
        self.assertEqual(fb.student.student.username, "Bob")

#Could add test for testing if feedback given time is the current time

class LecturerTestCase(TestCase):

    def setUp(self):
        add_course("Systems Programming 3", "SP3", "Introduction to Systems Programming using C and C++")
        add_lecturer("Wolf", "00001", "star", "wolf@star.com", ["SP3"])

    def test_lecturer_in_course(self):
        course = Course.objects.get(course_code = "SP3")
        testUser = User.objects.get(username = "Wolf")
        testLecturer = LecturerProfile.objects.get(lecturer=testUser)
        self.assertEqual(course.lecturer, testLecturer)

    def test_course_in_lecturer(self):
        course = Course.objects.get(course_code = "SP3")
        testUser = User.objects.get(username = "Wolf")
        testLecturer = LecturerProfile.objects.get(lecturer=testUser)
        self.assertTrue(course in testLecturer.course_set.all())

    def test_lecturer_email_correct(self):
        testUser = User.objects.get(username = "Wolf")
        testLecturer = LecturerProfile.objects.get(lecturer=testUser)
        self.assertEqual(testLecturer.lecturer.email, "wolf@star.com")


class CategoryTestCase(TestCase):

    def setUp(self):
        add_category("listening")

    def test_category_added_to_db(self):
        self.assertTrue(Category.objects.filter(name="listening").exists())


class MessageTestCase(TestCase):

    def setUp(self):
        add_category("listening")
        add_message("listening", "listened well")

    def test_message_correct(self):
        message = Message.objects.get(category="listening")
        self.assertEqual(message.text, "listened well")

    def test_cat_in_message(self):
        message = Message.objects.get(category="listening")
        cat = Category.objects.get(name="listening")
        self.assertEqual(message.category, cat)

    def test_default_message(self):
        #TODO
        self.assertTrue(True)



        

