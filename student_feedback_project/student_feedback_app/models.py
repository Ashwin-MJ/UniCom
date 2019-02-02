from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

import datetime
import random, string

class User(AbstractUser):
    # The default AbstractUser model provided by Django is used as this will be ideal for
    # authentication. Fields such as username,password,email and field are stored
    # in this. Fields below are added to this provided model to allow customisation.
    slug = models.SlugField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures', default="profile_pictures/default_image.jpg", blank=True)
    id_number = models.CharField(max_length=20,  unique=True)
    username = models.CharField(max_length=25,  unique=True)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

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
            emails = []
            superusers = User.objects.filter(is_superuser=True)
            for superuser in superusers:
                emails.append(superuser.email)

            message = 'Lecturer ' + instance.username + ' has registered and needs approval. Approve profiles @ feedbackapp.pythonanywhere.com/admin'

            send_mail('Lecturer needs approval',message,'lect.acc.unicom@gmail.com',emails)

        else :
            instance.is_active = True
            instance.is_student = True
            instance.save()
            StudentProfile.objects.create(student=instance)
            instance.studentprofile.save()


class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    score = models.IntegerField(default=0)
    courses = models.ManyToManyField('Course')
    degree = models.CharField(max_length=40, default="Degree not specified")
    bio = models.CharField(max_length=250, default="Biography not specified")

    def __lt__(self, other):
        return self.student.username < other.student.username

    def __gt__(self, other):
        return self.student.username > other.student.username

    def __eq__(self, other):
        return self.student.username == other.student.username

    def get_score_for_course(self,course):
        score = 0
        for fb in self.feedback_set.all():
            if fb.which_course.subject == course:
                score += fb.points
        return score

    def get_top_attributes(self):
        scores = {}
        for fb in self.feedback_set.all():
            if fb.category not in scores:
                scores[fb.category] = fb.points
            else:
                scores[fb.category] += fb.points

        scores = [(k, scores[k]) for k in sorted(scores, key=scores.get, reverse=True)]
        return scores

    def get_weaknesses(self):
        scores = self.get_top_attributes()
        scores.reverse()
        if len(scores) > 4:
            scores = scores[:4]
        return scores

    def get_fb_for_course(self,course):
        fb_for_course = []
        for fb in self.feedback_set.all():
            if fb.which_course.subject == course:
                fb_for_course += [fb]

        return fb_for_course

    def get_courses_with_score(self):
        courses_with_score = {}
        for course in self.courses.all():
            courses_with_score[course] = self.get_score_for_course(course.subject)

        return courses_with_score

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
        size = 4
        chars = string.ascii_uppercase + string.digits
        cT = ''.join(random.choice(chars) for _ in range(size))
        # checking all other courses
        for course in Course.objects.all():
            # Checking if the course token on already existing course is the same as new one
            if cT == course.course_token:
                cT = self.token_gen()

        return self.subject_slug.upper()+cT

    def get_students_with_score(self):
        temp_dict = {}
        for each_stud in self.students.all():
            temp_dict[each_stud] = each_stud.get_score_for_course(self.subject)
        return temp_dict

    def get_leaderboard(self):
        temp_dict = self.get_students_with_score()
        # The dictionary stored in the retrieved dictionary has
        # each student as key and their score for this course as value
        # To get leaderboard, simply sort this dictionary by value and reverse
        temp_dict = [(k, temp_dict[k]) for k in sorted(temp_dict, key=temp_dict.get, reverse=True)]
        # Note that context_dict['sorted_students'] is saved as an array with format:
        # [(<StudentProfile: StudentProfile object (X)>, Y),
        #   (<StudentProfile: StudentProfile object (X)>, Y),
        #   ...
        #   ]
        # This is important in the template
        return temp_dict


class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

    def get_my_students(self):
        students = Course.objects.none()
        for course in self.course_set.all():
            students = students | course.students.all()
        return students.distinct()
    # Can access lecturers courses using LecturerProfile.course_set.all()
    # Can access lecturers feedback using LectureProfile.feedback_set.all()

class Feedback(models.Model):
    date_given = models.DateTimeField(default=timezone.now)
    feedback_id = models.IntegerField(primary_key=True,default=0)
    pre_defined_message = models.ForeignKey('Message',on_delete=models.CASCADE,null=True,blank=True) # Selected from a pre defined list depending on selected category
    points = models.IntegerField(default=0)
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    datetime_given = models.DateTimeField(default=timezone.now, blank=False)
    optional_message = models.CharField(max_length=200,default="")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def is_recent(self):
        return timezone.now() - self.datetime_given < datetime.timedelta(minutes=5)

    def from_student(self):
        # Helper function to allow you to identify if a feedback is provided from a student
        return self.from_user.is_student and not self.from_user.is_lecturer

    def from_lecturer(self):
        # Helper function to allow you to identify if a feedback is provided from a lecturer
        return self.from_user.is_lecturer and not self.from_user.is_student

class Category(models.Model):
    name = models.CharField(max_length=20, default="Empty",primary_key=True)

    # Store the hex code for the colour field as a CharField. This can then be retrieved and
    # used later as required
    colour = models.CharField(max_length=6, default="#009999")
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
    student_id = models.IntegerField(primary_key=True,default=0)
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_with_student"

class Feedback_with_from_user(models.Model):
    fromUserName = models.CharField(max_length=200,default="No giving user")
    from_user_id = models.IntegerField(primary_key=True,default=0)
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_with_from_user"

class Feedback_with_course(models.Model):
    courseName = models.CharField(max_length=200,default="No course")
    date_given = models.DateTimeField(default=timezone.now)
    feedback_id = models.IntegerField(primary_key=True,default=0)
    pre_defined_message_id = models.CharField(max_length=200,default="No message")
    points = models.IntegerField(default=0)
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, null=True, blank=True)
    which_course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    datetime_given = models.DateTimeField(default=timezone.now, blank=False)
    optional_message = models.CharField(max_length=200,default="")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_with_course"
