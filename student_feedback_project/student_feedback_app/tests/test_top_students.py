from django.test import Client
from django.test import TestCase
from populate import *


class TopStudentsTestCase(TestCase):
    fixtures=['student_feedback_app']

    def test_lecturer_courses_html_dict_length_is_five(self):
        c = Client()
        c.login(username="00001", password="password")
        response = c.get("/lecturer/courses/")
        self.assertTrue(len(response.context['sorted_students']) == 5)

    def test_lecturer_courses_html_dict_order_of_students(self):
        c = Client()
        c.login(username="00001", password="password")
        response = c.get("/lecturer/courses/")
        student_list = response.context['sorted_students']
        actual_points_list = list()
        for student in student_list:
            actual_points_list.append(student[1])
        expected_points_list = [40,16,5,5,4]
        self.assertListEqual(actual_points_list, expected_points_list)
