from dal import autocomplete
from django import forms
from .models import Course,Feedback,User,Category,Message
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
    optional_message = forms.CharField(max_length=200, help_text="Optional Message")
    points = forms.IntegerField(max_value=5,min_value=0, help_text="Points")
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                        widget=autocomplete.ModelSelect2(
                                            'category_autocomplete'
                                        ),
                                        help_text="Category"
                                    )
    pre_defined_message = forms.ModelChoiceField(queryset=Message.objects.all(), help_text="Pre Defined Message")

    class Meta:
        model = Feedback
        fields = ('category', 'pre_defined_message','optional_message','points')
