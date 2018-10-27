from django.db import models

class Student(models.Model):
	username = models.CharField(max_length=40, primary_key=True)
	usernameSlug = models.SlugField(max_length=50)
	password = models.CharField(max_length=40)
	email = models.EmailField()
	profile_picture = models.ImageField(null=True, blank=True)
	score = models.IntegerField(default=0)
	classes = models.ManyToManyField(Class, on_delete=models.CASCADE)

class Class(models.Model):
	subject = models.CharField(max_length=40, primary_key=True)
	students = ManyToManyField(Student, on_delete=models.CASCADE)
	lecturer = ForeignKey(Lecturer, on_delete=models.CASCADE)
	leaderboard = ManyToManyField(Student, on_delete=models.CASCADE)

class Lecturer(models.Model):
	username = models.CharField(max_length=40, primary_key=True)
	usernameSlug = models.SlugField(max_length=50)
	password = models.CharField(max_length=40)
	email = models.EmailField()
	profile_picture = models.ImageField(null=True, blank=True)
	classes = models.ManyToManyField(Class, on_delete=models.CASCADE)

class Feedback(models.Model):
	category = models.CharField(max_length=100)
	points = models.IntegerField(default=0)
	lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
