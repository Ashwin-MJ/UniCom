from rest_framework import serializers
from student_feedback_app.models import *

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('date_given', 'feedback_id', 'pre_defined_message',
                  'points', 'lecturer_id', 'student_id',
                  'which_course_id', 'datetime_given', 'optional_message',
                  'category_id')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')

class Feedback_with_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_category
        fields = ('categoryName', 'feedback_id')

class Feedback_with_studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_student
        fields = ('studentName', 'feedback_id')
