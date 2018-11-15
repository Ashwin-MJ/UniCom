from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone


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
    classes = models.ManyToManyField('Class')

class Class(models.Model):
    subject = models.CharField("Subject", max_length=40,)
    class_description = models.CharField(max_length=200, default="")
    subject_slug = models.SlugField(max_length=50, default='empty_slug')
    students = models.ManyToManyField('StudentProfile')#, null=True, blank=True)
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    class_code = models.CharField(max_length=20, primary_key=True)
    class_token = models.CharField(max_length=7, default = "")
    def save(self, *args, **kwargs):
        self.subject_slug = slugify(self.class_code)
        super(Class, self).save(*args, **kwargs)


class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    # Can access lecturers classes using LecturerProfile.class_set.all()
    # Can access lecturers feedback using LectureProfile.feedback_set.all()

class Feedback(models.Model):
<<<<<<< HEAD
        feedback_id = models.IntegerField(primary_key=True,default=0)
        date_given = models.DateTimeField(default=timezone.now)
        message = models.CharField(max_length=200,default="No message")
        category = models.CharField(max_length=100)
        points = models.IntegerField(default=0)
        lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
        student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
        which_class = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True)

=======
    feedback_id = models.IntegerField(primary_key=True,default=0)
    message = models.CharField(max_length=200,default="No message")
    points = models.IntegerField(default=0)
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_class = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now, blank=False)

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=20, default="Empty")

    def __str__(self):
        return self.name
>>>>>>> 99a46b62d3d15fb888ecaa6268c581e491952b28
