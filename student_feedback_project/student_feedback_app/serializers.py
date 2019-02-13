from rest_framework import serializers
from student_feedback_app.models import *

class Feedback_with_courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_course
        fields = ('courseName', 'date_given', 'feedback_id', 'pre_defined_message_id',
                  'points', 'from_user', 'student',
                  'which_course', 'datetime_given', 'optional_message',
                  'category')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')

class Feedback_with_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_category
        fields = ('categoryColour', 'feedback_id')

class Feedback_with_studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_student
        fields = ('studentName', 'student_id')

class Feedback_with_from_userSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_from_user
        fields = ('fromUserName', 'from_user_id')
