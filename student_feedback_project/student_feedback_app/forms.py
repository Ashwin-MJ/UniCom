from django import forms
from .models import Class


class classForm(forms.ModelForm):
    subject = forms.CharField(max_length=40, help_text="Class Name")
    class_description = forms.CharField(max_length=200, required=False, help_text="Class Description")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Class
        fields = ('subject', 'class_description',)

