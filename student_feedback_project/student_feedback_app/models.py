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
    date_given = models.DateTimeField(default=timezone.now)
    feedback_id = models.IntegerField(primary_key=True,default=0)
    message = models.CharField(max_length=200,default="No message")
    points = models.IntegerField(default=0)
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_class = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=20, default="Empty")

    def __str__(self):
        return self.name

class Feedback_with_category(models.Model):
    categoryName = models.CharField(max_length=200,default="No category")
    feedback_id = models.IntegerField(primary_key=True,default=0)
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_with_category"

class Feedback_with_student(models.Model):
    studentName = models.CharField(max_length=200,default="No student")
    feedback_id = models.IntegerField(primary_key=True,default=0)
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_with_student"

class Feedback_with_class(models.Model):
    className = models.CharField(max_length=200,default="No class")
    date_given = models.DateTimeField(default=timezone.now)
    feedback_id = models.IntegerField(primary_key=True,default=0)
    message = models.CharField(max_length=200,default="No message")
    points = models.IntegerField(default=0)
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_class = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_with_class"
    


