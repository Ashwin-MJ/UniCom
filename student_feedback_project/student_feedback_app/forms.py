from dal import autocomplete
from django import forms

from .models import Course,Feedback,User,Category,Message
import datetime
from django.contrib.auth.forms import UserCreationForm#,AuthenticationForm


class CourseForm(forms.ModelForm):
    subject = forms.CharField(max_length=40, help_text="Course Name", required=False)
    course_code = forms.CharField(max_length=20, help_text= 'Course Code', required=True)
    course_description = forms.CharField(max_length=200, required=False, help_text="Course Description")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Course
        fields = ('subject', 'course_code', 'course_description',)


class FeedbackForm(autocomplete.FutureModelForm):
    optional_message = forms.CharField(max_length=200, required=False, help_text="Optional Message")
    points = forms.IntegerField(max_value=5,min_value=0, help_text="Points")

    class Meta:
        model = Feedback
        fields = ('category', 'pre_defined_message','optional_message','points')
        widgets = {
            'pre_defined_message': autocomplete.ModelSelect2(url='message_autocomplete',forward=['category']),
            'category': autocomplete.ModelSelect2(url='category_autocomplete')
        }
        help_texts = {
            'pre_defined_message': "Select a Message",
            'category': 'Category'
        }

class RegisterForm(UserCreationForm):
    is_lecturer = forms.ChoiceField(choices=[(1,'lecturer'),
         (0,'student')], widget=forms.RadioSelect(), label='Sign up as:')
    is_student = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = User
        fields = ('id_number', 'username', 'email', 'password1', 'password2', 'is_lecturer', 'is_student')

class addCourseForm(forms.ModelForm):
    course_token = forms.CharField(max_length= 7, help_text="Provided Course Token", required=True)

    class Meta:
        model = Course
        fields = ('course_token',)
