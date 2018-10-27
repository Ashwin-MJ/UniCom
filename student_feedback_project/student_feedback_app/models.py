from django.db import models

class Student(models.Model):
	username = models.CharField(max_length=40, primary_key=True)
	student_slug = models.SlugField(max_length=50)
	password = models.CharField(max_length=40)
	email = models.EmailField()
	profile_picture = models.ImageField(null=True, blank=True)
	score = models.IntegerField(default=0)
	classes = models.ManyToManyField('student_feedback_app.Class')

class Class(models.Model):
	subject = models.CharField(max_length=40, primary_key=True)
	students = models.ManyToManyField('student_feedback_app.Student')
	lecturer = models.ForeignKey('student_feedback_app.Lecturer', on_delete=models.CASCADE)

class Lecturer(models.Model):
	username = models.CharField(max_length=40, primary_key=True)
	lecturer_slug = models.SlugField(max_length=50)
	password = models.CharField(max_length=40)
	email = models.EmailField()
	profile_picture = models.ImageField(null=True, blank=True)
	classes = models.ManyToManyField(Class, related_name='taught_classes')

class Feedback(models.Model):
	category = models.CharField(max_length=100)
	points = models.IntegerField(default=0)
	lecturer = models.ForeignKey('student_feedback_app.Lecturer', on_delete=models.CASCADE)
	student = models.ForeignKey('student_feedback_app.Student', on_delete=models.CASCADE)
