from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime
import random, string

class User(AbstractUser):
    # The default AbstractUser model provided by Django is used as this will be ideal for
    # authentication. Fields such as username,password,email and field are stored
    # in this. Fields below are added to this provided model to allow customisation.
    slug = models.SlugField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures', default="profile_pictures/default_image.jpg", blank=True)
    id_number = models.CharField(max_length=20,  unique=True)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['username', 'email']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_lecturer:
            LecturerProfile.objects.create(lecturer=instance)
            instance.lecturerprofile.save()
        else :
            instance.is_student = True
            instance.save()
            StudentProfile.objects.create(student=instance)
            instance.studentprofile.save()


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
        self.course_token = self.token_gen()
        super(Course, self).save(*args, **kwargs)

    def token_gen(self):
        size = 7
        chars = string.ascii_uppercase + string.digits
        cT = ''.join(random.choice(chars) for _ in range(size))
        # checking all other courses
        for course in Course.objects.all():
            # Checking if the course token on already existing course is the same as new one
            if cT == course.course_token:
                cT = self.token_gen()

        return cT

class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    # Can access lecturers courses using LecturerProfile.course_set.all()
    # Can access lecturers feedback using LectureProfile.feedback_set.all()

class Feedback(models.Model):
    date_given = models.DateTimeField(default=timezone.now)
    feedback_id = models.IntegerField(primary_key=True,default=0)
    pre_defined_message = models.ForeignKey('Message',on_delete=models.CASCADE,null=True,blank=True) # Selected from a pre defined list depending on selected category
    points = models.IntegerField(default=0)
    lecturer = models.ForeignKey('LecturerProfile', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    datetime_given = models.DateTimeField(default=timezone.now, blank=False)
    optional_message = models.CharField(max_length=200,default="")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def is_recent(self):
        return timezone.now() - self.datetime_given < datetime.timedelta(minutes=5)

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
    



