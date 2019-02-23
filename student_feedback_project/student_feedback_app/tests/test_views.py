from django.test import TestCase
from django.urls import reverse

from populate import *

class MyProfileViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def login(self):
        # Helper method to login
        login = self.client.login(username="00001",password="password")
        response = self.client.get(reverse('my_profile'))
        return response

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)

    def test_error_if_not_logged_in(self):
        response = self.client.get(reverse('my_profile'))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertTrue(response.context['error'] == "auth")

    def test_logged_in_correct(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_feedback_app/general/my_profile.html')

    def test_correct_courses(self):
        response = self.login()
        # Get correct courses using models
        user = User.objects.get(id_number="00001")
        lect = LecturerProfile.objects.get(lecturer=user)
        courses = lect.courses.all()
        # Get list of courses found in response
        response_courses_list = list(response.context['courses'].keys())

        for course in courses:
            # Ensure all courses are present in response
            self.assertTrue(course in response_courses_list)

    def test_response_contains_edit_option(self):
        response = self.login()
        self.assertContains(response, "Edit Bio")

class ViewProfileViewTest(TestCase):
    fixtures = ['student_feedback_app']

    def login_lecturer(self):
        # Helper method to login as a lecturer
        login = self.client.login(username="00001",password="password")
        response = self.client.get(reverse('view_profile',kwargs={'student_number':1402781}))
        return response

    def login_student(self):
        # Helper method to login as a student
        login = self.client.login(username="1402001",password="password")
        response = self.client.get(reverse('view_profile',kwargs={'student_number':1402781}))
        return response

    def test_error_if_not_logged_in(self):
        response = self.client.get(reverse('view_profile',kwargs={'student_number':1402781}))
        self.assertTemplateUsed(response, 'student_feedback_app/general/error_page.html')
        self.assertTrue(response.context['error'] == "auth")

    def test_view_as_lecturer(self):
        response = self.login_lecturer()
        # When logged in as a lecturer, they should be able to see all feedback
        stud_user = User.objects.get(id_number=1402781)
        stud = StudentProfile.objects.get(student=stud_user)

        stud_all_fb = stud.feedback_set.all()

        for fb in stud_all_fb:
            self.assertTrue(fb in response.context['feedback'])

    def test_view_as_student(self):
        response = self.login_student()
        # When logged in as a student, they should only be able to see feedback they have given
        for fb in response.context['feedback']:
            self.assertTrue(fb.from_user.id_number == "1402001")
