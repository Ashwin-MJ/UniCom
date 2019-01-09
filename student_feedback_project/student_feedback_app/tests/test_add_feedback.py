from django.test import TestCase
from student_feedback_app.models import *
from student_feedback_app.forms import FeedbackForm

class CategoryAndMessageModelTestCase(TestCase):

    def setUp(self):
        # Set up a few categories and pre defined messages
        speaking = Category(name="Speaking")
        listening = Category(name="Listening")
        speaking.save()
        listening.save()
        speak_message = Message(category=speaking,
                                text="Good speech today!")
        list_message = Message(category=listening,
                                text="Thanks for paying attention today")
        speak_message.save()
        list_message.save()

    def test_categories_saved(self):
        self.assertTrue(Category.objects.get(name="Speaking"))
        self.assertTrue(Category.objects.get(name="Listening"))

    def test_messages_saved(self):
        self.assertTrue(Message.objects.get(text="Thanks for paying attention today"))
        self.assertTrue(Message.objects.get(text="Good speech today!"))

    def test_message_has_correct_category(self):
        list_message = Message.objects.get(text="Thanks for paying attention today")
        speak_message = Message.objects.get(text="Good speech today!")

        self.assertEqual(list_message.category.name, "Listening")
        self.assertEqual(speak_message.category.name, "Speaking")

    def test_get_messages_by_category(self):
        speaking = Category.objects.get(name="Speaking")
        listening = Category.objects.get(name="Listening")
        list_message = Message.objects.get(text="Thanks for paying attention today")
        speak_message = Message.objects.get(text="Good speech today!")

        self.assertEqual(len(speaking.message_set.all()), 1)
        self.assertTrue(speaking.message_set.get(text="Good speech today!"))
        self.assertNotIn(list_message,speaking.message_set.all())

        self.assertEqual(len(listening.message_set.all()), 1)
        self.assertTrue(listening.message_set.get(text="Thanks for paying attention today"))
        self.assertNotIn(speak_message,listening.message_set.all())

class IndividualFeedbackTestCase(TestCase):

    def setUp(self):
        stud_user = User(id_number="1234",username="Student",is_student=True)
        lect_user = User(id_number="5678", username="Prof Lecturer",is_lecturer=True)
        stud_user.save()
        lect_user.save()

        stud = StudentProfile(student=stud_user)
        lect = LecturerProfile(lecturer=lect_user)
        stud.save()
        lect.save()

        speaking = Category(name="Speaking")
        speaking.save()

        speak_message = Message(category=speaking,
                                text="Good speech today!")
        speak_message.save()

        course = Course(subject="Systems Programming 3",
                        course_description="Introduction to Systems Programming using C and C++",
                        course_code="SP3")
        course.save()

    def test_feedback_form_true(self):
        form_data = { "optional_message": "You made excellent points about ...",
                        "category" : "Speaking",
                        "points" : 5,
                        "pre_defined_message" : "Good speech today!"}

        fb_form = FeedbackForm(data=form_data)
        self.assertTrue(fb_form.is_valid())

    def test_feedback_form_false(self):
        form_data = { "optional_message": "You were top of the class!",
                        "category" : "Participation",
                        "points" : 5,
                        "pre_defined_message" : "Great marks in the quiz"}

        fb_form = FeedbackForm(data=form_data)
        # This test should fail as the category Participation and the pre defined message
        # is not saved in the database
        self.assertFalse(fb_form.is_valid())

    def test_feedback_saved_for_student(self):
        fb = Feedback(optional_message="You made excellent points about ...",
                        category=Category.objects.get(name="Speaking"),
                        points=5,
                        pre_defined_message=Message.objects.get(text="Good speech today!"),
                        student=StudentProfile.objects.get(student=User.objects.get(id_number="1234")),
                        lecturer=LecturerProfile.objects.get(lecturer=User.objects.get(id_number="5678")),
                        which_course=Course.objects.get(course_code="SP3"))
        fb.save()
        stud = StudentProfile.objects.get(student=User.objects.get(id_number="1234"))

        self.assertEqual(len(stud.feedback_set.all()),1)
        self.assertEqual(stud.feedback_set.all()[0].optional_message, "You made excellent points about ...")


#class GroupFeedbackTestCase(TestCase):

#    def test_feedback_created(self):
        # Ensure that a feedback object is saved correctly in the database
        #fb = Feedback()

        # Upon clicking "Submit Feedback" ensure the feedback is created correctly

    # Ensure that upon submitting group feedback, that feedback is given to
    # all students
