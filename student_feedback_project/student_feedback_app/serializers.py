from rest_framework import serializers
from student_feedback_app.models import *

class Feedback_with_courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_course
        fields = ('courseName', 'date_given', 'feedback_id', 'pre_defined_message_id',
                  'points', 'lecturer', 'student',
                  'which_course', 'datetime_given', 'optional_message',
                  'category')

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
        fields = ('studentName', 'student_id')

class Feedback_with_lecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback_with_lecturer
        fields = ('lecturerName', 'lecturer_id')
