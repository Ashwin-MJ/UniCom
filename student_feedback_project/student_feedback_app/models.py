from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class StudentProfile(models.Model):
        student = models.OneToOneField(User, on_delete=models.CASCADE)
        # The default User model provided by Django is used as this will be ideal for
        # authentication. Fields such as username,password,email and field are stored
        # in this.
        student_slug = models.SlugField(max_length=50)
        student_number = models.CharField(max_length=20, primary_key=True)
        profile_picture = models.ImageField(upload_to='profile_pictures', default="profile_pictures/default_image.jpg", blank=True)
        score = models.IntegerField(default=0)
        classes = models.ManyToManyField('Class')

        def save(self, *args, **kwargs):
            self.student_slug = slugify(self.student.username)
            super(StudentProfile, self).save(*args, **kwargs)

class Class(models.Model):
        subject = models.CharField(max_length=40)
        class_description = models.CharField(max_length=200, default="")
        subject_slug = models.SlugField(max_length=50, default='empty_slug')
        students = models.ManyToManyField('StudentProfile')#, null=True, blank=True)
        lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
        class_code = models.CharField(max_length=20, primary_key=True)

        def save(self, *args, **kwargs):
            self.subject_slug = slugify(self.class_code)
            super(Class, self).save(*args, **kwargs)

class LecturerProfile(models.Model):
        lecturer = models.OneToOneField(User, on_delete=models.CASCADE)
        # The default User model provided by Django is used as this will be ideal for
        # authentication. Fields such as username,password,email and field are stored
        # in this.
        lecturer_number = models.CharField(max_length=20, primary_key=True)
        lecturer_slug = models.SlugField(max_length=50)
        profile_picture = models.ImageField(upload_to='profile_pictures', default="profile_pictures/default_image.jpg", blank=True)
        # Can access lecturers classes using LecturerProfile.class_set.all()
        # Can access lecturers feedback using LectureProfile.feedback_set.all()

        def save(self, *args, **kwargs):
            self.lecturer_slug = slugify(self.lecturer.username)
            super(LecturerProfile, self).save(*args, **kwargs)

class Feedback(models.Model):
        feedback_id = models.IntegerField(primary_key=True,default=0)
        message = models.CharField(max_length=200,default="No message")
        category = models.CharField(max_length=100)
        points = models.IntegerField(default=0)
        lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
        student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
        which_class = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True)
        datetime = models.DateTimeField(default=timezone.now, blank=False)
