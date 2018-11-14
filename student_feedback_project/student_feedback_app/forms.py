from django import forms
from .models import Course,Feedback,User,Category
import datetime

class CourseForm(forms.ModelForm):
    subject = forms.CharField(max_length=40, help_text="Course Name", required=False)
    course_code = forms.CharField(max_length=20, help_text= 'Course Code', required=True)
    course_description = forms.CharField(max_length=200, required=False, help_text="Course Description")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Course
        fields = ('subject', 'course_code', 'course_description',)


class FeedbackForm(forms.ModelForm):
    message = forms.CharField(max_length=200, help_text="Message")
    points = forms.IntegerField(max_value=5,min_value=0, help_text="Points")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text="Category")

    class Meta:
        model = Feedback
        fields = ('message','category', 'points')
