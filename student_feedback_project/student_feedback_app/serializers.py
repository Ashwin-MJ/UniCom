from rest_framework import serializers
from student_feedback_app.models import *

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('date_given', 'feedback_id', 'message',
                  'points', 'lecturer', 'student',
                  'which_class', 'category')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'id')

class Feedback_with_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_category
        fields = ('categoryName', 'feedback_id')

class Feedback_with_studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_student
        fields = ('studentName', 'feedback_id')
