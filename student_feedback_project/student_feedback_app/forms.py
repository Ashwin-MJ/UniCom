from dal import autocomplete
from django import forms
from .models import Course, Feedback, User, Category, Message
from django.contrib.auth.forms import UserCreationForm


class CourseForm(forms.ModelForm):
    subject = forms.CharField(max_length=40, help_text="Course Name", required=True)
    course_code = forms.CharField(max_length=20, help_text= 'Course Code', required=True)
    course_description = forms.CharField(max_length=200, required=True, help_text="Course Description")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Course
        fields = ('subject', 'course_code', 'course_description',)


class FeedbackForm(autocomplete.FutureModelForm):
    optional_message = forms.CharField(max_length=200, required=False, help_text="Optional Message")
    points = forms.IntegerField(max_value=5,min_value=0, help_text="Points", required=True)

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
    is_lecturer = forms.ChoiceField(choices=[(1,'Lecturer'),
         (0,'Student')], widget=forms.RadioSelect(), label='Sign up as:')
    is_student = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(label='Full Name:', required=False)

    class Meta:
        model = User
        fields = ('id_number', 'username', 'email', 'password1', 'password2', 'is_lecturer', 'is_student')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['id_number'].help_text = "This is your student number"
        self.fields['is_lecturer'].help_text = "You can either sign up as a student or a lecturer. If you choose to sign up as a lecturer, an administrator will need to accept your request before your account is activated"


class AddCourseForm(forms.ModelForm):
    course_token = forms.CharField(max_length= 20, help_text="Provided Course Token", required=True)

    class Meta:
        model = Course
        fields = ('course_token',)


class EditBioForm(forms.ModelForm):
    degree = forms.CharField(max_length=60, help_text="Degree", required=True)
    bio = forms.CharField(max_length=250, help_text= 'Bio', required=True)

    class Meta:
        model = User
        fields = ('degree', 'bio',)

class EditCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text="What would you like to change the name of this category to?")

    class Meta:
        model = Category
        fields = ('name',)

class NewCategoryForm(forms.ModelForm):
    new_name = forms.CharField(max_length=30, help_text="What should the new category be called?")

    class Meta:
        model = Category
        fields = ('new_name',)

class EditMessageForm(forms.ModelForm):
    text = forms.CharField(max_length=200, help_text="What would you like to change the text of this message to?")

    class Meta:
        model = Message
        fields = ('text',)

class NewMessageForm(forms.ModelForm):
    new_text = forms.CharField(max_length=200, help_text="Enter the text for the new message:")

    class Meta:
        model = Message
        fields = ('new_text',)
