from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.validators import int_list_validator

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
    degree = models.CharField(max_length=60, default="Degree not specified")
    bio = models.CharField(max_length=250, default="Biography not specified")
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

    #comparison based on username
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

    def get_score_for_category(self):
        scores = {}
        for fb in self.feedback_set.all():
            if fb.category not in scores:
                scores[fb.category] = fb.points
            else:
                scores[fb.category] += fb.points
        return scores

class Achievement(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    achiev = models.CharField(validators=[int_list_validator], max_length=100, default=0)

    def gen_achievement(self, attribute, score, user):
        self.category = Category.objects.get(name=attribute,user=user)
        if score >= 100:
            self.achiev = [100,50,25,10,5]
        elif score >= 50:
            self.achiev = [50,25,10,5]
        elif score >= 25:
            self.achiev = [25,10,5]
        elif score >= 10:
            self.achiev = [10,5]
        elif score >= 5:
            self.achiev = [5]
        else:
            self.achiev = [0]

class Course(models.Model):
    subject = models.CharField("Subject", max_length=40,)
    course_description = models.CharField(max_length=200, default="")
    subject_slug = models.SlugField(max_length=50, default='empty_slug')
    students = models.ManyToManyField('StudentProfile')
    lecturers = models.ManyToManyField('LecturerProfile')
    course_code = models.CharField(max_length=20, primary_key=True)
    course_token = models.CharField(max_length=20, default = "")

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

    # Used for the graph implementation, gives the total score for lecturers
    # categories in a course
    def get_total_for_course_attributes(self):
        fbTotals={}


        for feedback in self.feedback_set.all():

            if feedback.category.name in fbTotals:
                dates = []
                print(' ')
                print(feedback.category.name)
                for i in range(len(fbTotals[feedback.category.name])):


                    # populate dates with all the dates saved in fbTotal for this feedback category.
                    for data in fbTotals[feedback.category.name]:
                        for key in data:
                            if key not in dates:
                                dates.append(key)
                    print('////////////////////////')
                    print(dates)
                    print('////////////////////////')


                    # print('--------')
                    # print(fbTotals[feedback.category.name][i])
                    # print('--------')

                    if feedback.date_only in dates:
                        print('Date is same')
                        # print(feedback.category.name)
                        # print(feedback.points)
                        # print('Values for this cat: ', fbTotals[feedback.category.name][i].keys())
                        # print('new feedback date: ', feedback.date_only)
                        print(feedback.date_only)
                        print(fbTotals[feedback.category.name][i])
                        if feedback.date_only in fbTotals[feedback.category.name][i]:
                            fbTotals[feedback.category.name][i][feedback.date_only] += feedback.points
                        print(fbTotals[feedback.category.name])
                        # print(' ')
                    else:

                        print("new date")
                        # print(feedback.category.name)
                        # print(feedback.points)
                        # print('Values for this cat: ', fbTotals[feedback.category.name][i].keys())
                        # print('new feedback date: ', feedback.date_only)
                        fbTotals[feedback.category.name].append({feedback.date_only : feedback.points})
                        print(fbTotals[feedback.category.name])
                        # print(" ")


            else:
                print('category didnt exist')
                print(feedback.category.name)
                fbTotals[feedback.category.name] = [{feedback.date_only: feedback.points}]

        print('finished')
        # print(fbTotals)
        return fbTotals


class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    courses = models.ManyToManyField('Course')

    def get_my_students(self):
        students = Course.objects.none()
        for course in self.courses.all():
            students = students | course.students.all()
        return students.distinct()
    # Can access lecturers courses using LecturerProfile.course_set.all()
    # Can access lecturers feedback using LectureProfile.feedback_set.all()
    def get_courses_with_students(self):
        courses_with_students = {}
        for course in self.courses.all():
            courses_with_students[course] = len(course.students.all())
        return courses_with_students




class Feedback(models.Model):
    date_only = models.DateField(default=timezone.now)
    date_given = models.DateTimeField(default=timezone.now)
    feedback_id = models.IntegerField(primary_key=True)
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
    name = models.CharField(max_length=30, default="Empty")
    user = models.ForeignKey('User',on_delete=models.CASCADE,null=True)

    # Store the hex code for the colour field as a CharField. This can then be retrieved and
    # used later as required
    colour = models.CharField(max_length=7, default="#009999")
    # Can access messages associated with a given category using Category.message_set.all()

    def __str__(self):
        return self.name

class Message(models.Model):
    # This is a Message model for each pre defined message associate with a category
    # As per the client's requirements, a Lecturer should first select a category, after which a list of pre-defined messages associated with that category are displayed
    # The Lecturer MUST select one of these messages.
    category = models.ForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True)
    text = models.CharField(max_length=200,default="No message")
    user = models.ForeignKey('User',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.text

class Feedback_full(models.Model):
    feedback_id = models.IntegerField(primary_key=True, default=0)
    points = models.IntegerField(default=0)
    datetime_given = models.DateTimeField(default=timezone.now, blank=False)
    optional_message = models.CharField(max_length=200,default="")
    categoryColour = models.CharField(max_length=200,default="No category colour")
    categoryName = models.CharField(max_length=200, default="No category")
    preDefMessageText = models.CharField(max_length=200,default="No message")
    studentName = models.CharField(max_length=200,default="No student")
    courseName = models.CharField(max_length=200,default="No course")
    fromUserName = models.CharField(max_length=200,default="No from user")
    class Meta:
        managed = False
        db_table = "student_feedback_app_feedback_full"
