from rest_framework import serializers
from student_feedback_app.models import *

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('date_given', 'feedback_id', 'message',
                  'points', 'lecturer', 'student',
                  'which_class', 'category')
