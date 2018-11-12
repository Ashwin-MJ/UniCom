from django import forms
from .models import Class,Feedback,User,Category
import datetime

class classForm(forms.ModelForm):
    subject = forms.CharField(max_length=40, help_text="Class Name")
    class_description = forms.CharField(max_length=200, required=False, help_text="Class Description")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Class
        fields = ('subject', 'class_description',)


class FeedbackForm(forms.ModelForm):
    message = forms.CharField(max_length=200, help_text="Message")
    #category = forms.CharField(max_length=100, help_text="Category")
    points = forms.IntegerField(max_value=5,min_value=0, help_text="Points")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text="Category")

    class Meta:
        model = Feedback
        #fields = ('message','category','points')
        fields = ('message','category', 'points')
