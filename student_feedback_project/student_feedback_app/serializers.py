from rest_framework import serializers
from student_feedback_app.models import *

class Feedback_fullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_full
        fields = ('points', 'datetime_given', 'optional_message', 'categoryColour', 'categoryName',
                  'preDefMessageText', 'studentName', 'courseName', 'fromUserName')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('date_given', 'feedback_id', 'pre_defined_message', 'points', 'from_user',
                    'student', 'which_course', 'datetime_given', 'optional_message', 'category')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'user', 'colour', 'message_set')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('category', 'text', 'user')
