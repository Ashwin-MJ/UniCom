from django.db import models
import uuid

class Student(models.Model):
        username = models.CharField(max_length=40)
        student_slug = models.SlugField(max_length=50)
        student_nb = models.CharField(max_length=20, primary_key=True, default=uuid.uuid1);
        password = models.CharField(max_length=40)
        email = models.EmailField()
        profile_picture = models.ImageField(null=True, blank=True)
        score = models.IntegerField(default=0)
        classes = models.ManyToManyField('student_feedback_app.Class')
        managed = True;

class Class(models.Model):
        subject = models.CharField(max_length=40)
        students = models.ManyToManyField('student_feedback_app.Student', null=True, blank=True)
        lecturer = models.ForeignKey('student_feedback_app.Lecturer', on_delete=models.CASCADE, null=True, blank=True)
        unique_code = models.CharField(max_length=20, primary_key=True, default=uuid.uuid1)
        managed = True;

class Lecturer(models.Model):
        username = models.CharField(max_length=40, primary_key=True, default=uuid.uuid1)
        lecturer_slug = models.SlugField(max_length=50)
        password = models.CharField(max_length=40)
        email = models.EmailField()
        profile_picture = models.ImageField(null=True, blank=True)
        classes = models.ManyToManyField(Class, related_name='taught_classes')
        managed = True;

class Feedback(models.Model):
        category = models.CharField(max_length=100)
        points = models.IntegerField(default=0)
        lecturer = models.ForeignKey('student_feedback_app.Lecturer', on_delete=models.CASCADE)
        student = models.ForeignKey('student_feedback_app.Student', on_delete=models.CASCADE)
        managed = True;
