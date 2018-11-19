from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


class User(AbstractUser):
    # The default AbstractUser model provided by Django is used as this will be ideal for
    # authentication. Fields such as username,password,email and field are stored
    # in this. Fields below are added to this provided model to allow customisation.
    slug = models.SlugField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures', default="profile_pictures/default_image.jpg", blank=True)
    id_number = models.CharField(max_length=20)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)


class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    score = models.IntegerField(default=0)
    courses = models.ManyToManyField('Course')

class Course(models.Model):
    subject = models.CharField("Subject", max_length=40,)
    course_description = models.CharField(max_length=200, default="")
    subject_slug = models.SlugField(max_length=50, default='empty_slug')
    students = models.ManyToManyField('StudentProfile')
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    course_code = models.CharField(max_length=20, primary_key=True)
    course_token = models.CharField(max_length=7, default = "")

    def save(self, *args, **kwargs):
        self.subject_slug = slugify(self.course_code)
        super(Course, self).save(*args, **kwargs)


class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    # Can access lecturers courses using LecturerProfile.course_set.all()
    # Can access lecturers feedback using LectureProfile.feedback_set.all()

class Feedback(models.Model):
    feedback_id = models.IntegerField(primary_key=True,default=0)
    pre_defined_message = models.ForeignKey('Message',on_delete=models.CASCADE,null=True,blank=True) # Selected from a pre defined list depending on selected category
    points = models.IntegerField(default=0)
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    datetime_given = models.DateTimeField(default=timezone.now, blank=False)
    optional_message = models.CharField(max_length=200,default="")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=20, default="Empty",primary_key=True)
    # Can access messages associated with a given category using Category.message_set.all()

    def __str__(self):
        return self.name

class Message(models.Model):
    # This is a Message model for each pre defined message associate with a category
    # As per the client's requirements, a Lecturer should first select a category, after which a list of pre-defined messages associated with that category are displayed
    # The Lecturer MUST select one of these messages.
    category = models.ForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True)
    text = models.CharField(max_length=200,default="No message",primary_key=True)

    def __str__(self):
        return self.text
