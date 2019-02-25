from django.test import TestCase
from django.urls import reverse

from populate import *

def login_lecturer(self):
    # Helper method to login as a lecturer
    login = self.client.login(username="00001",password="password")
    return login

def login_student(self):
    # Helper method to login as a studentx
    login = self.client.login(username="1402001",password="password")
    return login

class MyProfileViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)

    def test_error_if_not_logged_in(self):
        response = self.client.get(reverse('my_profile'))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertTrue(response.context['error'] == "auth")

    def test_logged_in_lect_correct(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/general/my_profile.html')

    def test_logged_in_stud_correct(self):
        login = login_student(self)
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/general/my_profile.html')

    def test_correct_courses(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('my_profile'))
        # Get correct courses using models
        user = User.objects.get(id_number="00001")
        lect = LecturerProfile.objects.get(lecturer=user)
        courses = lect.courses.all()
        # Get list of courses found in response
        response_courses_list = list(response.context['courses'].keys())
        for course in courses:
            # Ensure all courses are present in response
            self.assertIn(course,response_courses_list)

    def test_response_contains_edit_option(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('my_profile'))
        self.assertContains(response, "Edit Bio")

class ViewProfileViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_error_if_not_logged_in(self):
        response = self.client.get(reverse('view_profile',kwargs={'student_number':1402781}))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertTrue(response.context['error'] == "auth")

    def test_view_as_lecturer(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('view_profile',kwargs={'student_number':1402781}))

        # When logged in as a lecturer, they should be able to see all feedback
        stud_user = User.objects.get(id_number=1402781)
        stud = StudentProfile.objects.get(student=stud_user)
        stud_all_fb = stud.feedback_set.all()

        for fb in stud_all_fb:
            self.assertIn(fb, response.context['feedback'])

    def test_view_as_student(self):
        login = login_student(self)
        response = self.client.get(reverse('view_profile',kwargs={'student_number':1402781}))

        # When logged in as a student, they should only be able to see feedback they have given
        for fb in response.context['feedback']:
            self.assertEqual(fb.from_user.id_number,"1402001")

class StudentHomeViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_error_if_lecturer(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('student_home'))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertEqual(response.context['error'],"auth")

class StudentAllFeedbackViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_error_if_lecturer(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('student_all_feedback'))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertEqual(response.context['error'],"auth")

    def test_top_four_attributes(self):
        login = login_student(self)
        response = self.client.get(reverse('student_all_feedback'))
        self.assertTemplateUsed(response, 'student_feedback_app/student/student_all_feedback.html')
        self.assertTrue(len(response.context['top_attributes']) <= 4)

class StudentCoursesViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_error_if_lecturer(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('student_courses'))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertEqual(response.context['error'],"auth")

    def test_logged_in_stud_correct(self):
        login = login_student(self)
        response = self.client.get(reverse('student_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/student/student_courses.html')

class StudentCourseViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_course_does_not_exist(self):
        login = login_student(self)
        response = self.client.get(reverse('student_course',kwargs={'subject_slug': "random"}))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertEqual(response.context['error'],"no_course")

class StudentAddIndividualFeedbackViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_error_if_lecturer(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('student_add_individual_feedback',kwargs={'subject_slug': "arh01",'student_number':1402781}))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertEqual(response.context['error'],"auth")

    def test_logged_in_stud_correct(self):
        login = login_student(self)
        response = self.client.get(reverse('student_add_individual_feedback',kwargs={'subject_slug': "arh01",'student_number':1402781}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/student/student_add_individual_feedback.html')

    def test_student_does_not_exist(self):
        login = login_student(self)
        response = self.client.get(reverse('student_add_individual_feedback',kwargs={'subject_slug': "arh01",'student_number':1234567}))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertEqual(response.context['error'],"no_student")


class MyProvidedFeedbackViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_stud_correct(self):
        login = login_student(self)
        response = self.client.get(reverse('student_provided_feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/student/student_provided_feedback.html')

    def test_lect_correct(self):
        login = login_lecturer(self)
        response = self.client.get(reverse('lecturer_provided_feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/lecturer/lecturer_provided_feedback.html')

    def test_error_if_not_logged_in(self):
        response = self.client.get(reverse('student_provided_feedback'))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertTrue(response.context['error'] == "auth")

class LecturerHomeViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def test_student_redirect(self):
        login = login_student(self)
        response = self.client.get(reverse('lecturer_home'))
        self.assertRedirects(response, '/student/home/')
