from django.test import Client
from django.test import TestCase
from populate import *


class LeaderboardTestCase(TestCase):
    fixtures=['student_feedback_app']

    # def test_lecturer_course_html_dict_length_is_five(self):
    #     c = Client()
    #     c.login(username="00001", password="password")
    #     response = c.get("/lecturer/courses/arh01/")
    #     self.assertTrue(len(response.context['sorted_students']) == 5)
    #
    # def test_lecturer_course_html_dict_order_of_students(self):
    #     c = Client()
    #     c.login(username="00001", password="password")
    #     response = c.get("/lecturer/courses/arh01/")
    #     student_list = response.context['sorted_students']
    #     actual_points_list = list()
    #     for student in student_list:
    #         actual_points_list.append(student[1])
    #     expected_points_list = [5,5,0,0,0]
    #     self.assertListEqual(actual_points_list, expected_points_list)

    def test_student_course_html_dict_length_is_five(self):
        c = Client()
        c.login(username="1402789", password="password")
        response = c.get("/student/courses/arh01/")
        self.assertTrue(len(response.context['sorted_students']) == 5)

    def test_student_course_html_dict_order_of_students(self):
        c = Client()
        c.login(username="1402789", password="password")
        response = c.get("/student/courses/arh01/")
        student_list = response.context['sorted_students']
        actual_points_list = list()
        for student in student_list:
            actual_points_list.append(student[1])
        expected_points_list = [5,5,0,0,0]
        self.assertListEqual(actual_points_list, expected_points_list)
