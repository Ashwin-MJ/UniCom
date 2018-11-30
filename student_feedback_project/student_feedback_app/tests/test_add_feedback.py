from django.test import TestCase
from student_feedback_app.models import Category,Message

# See test_models.py for an example test

class FeedbackModelTestCase(TestCase):

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

        self.assertEqual(len(speaking.message_set.all()), 1)
        self.assertTrue(speaking.message_set.get(text="Good speech today!"))

        self.assertEqual(len(listening.message_set.all()), 1)
        self.assertTrue(listening.message_set.get(text="Thanks for paying attention today"))

#class GroupFeedbackTestCase(TestCase):

#    def test_feedback_created(self):
        # Ensure that a feedback object is saved correctly in the database
        #fb = Feedback()

        # Upon clicking "Submit Feedback" ensure the feedback is created correctly

    # Ensure that upon submitting group feedback, that feedback is given to
    # all students
