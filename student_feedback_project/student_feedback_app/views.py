from django.shortcuts import render
from rest_framework.views import APIView
from student_feedback_app.serializers import *
from rest_framework import generics
from student_feedback_app.models import Feedback
from datetime import datetime, timedelta
from django.utils import timezone
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from .models import LecturerProfile,Feedback,Class,StudentProfile,User,Feedback_with_category,Feedback_with_student
from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.
def index(request):
    return HttpResponse("This is the homepage")

def student_home(request):
    context_dict = {}
    #get feedback given in this month; use __gt for '>'
    d = timezone.now().month
    feedback = Feedback.objects.filter(date_given__month=d)
    context_dict["feedback"] = Feedback.objects.all()                                     
    return render(request, 'student_feedback_app/student_home.html', 			context=context_dict)

def all_feedback(request):
    return HttpResponse("This page shows all of my feedback")


def my_classes(request):
    return HttpResponse("This page shows all of my classes")

def lecturer_home(request):
    context_dict = {}
    if request.user.is_lecturer:
        try:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            fb = lect.feedback_set.all().order_by('-date_given')
            classes = lect.class_set.all()
            context_dict['lecturer'] = lect
            context_dict['classes'] = classes
            context_dict['feedback'] = fb
        except:
            return HttpResponse('Something has gone wrong')
    else:
        return HttpResponse("You are not allowed here")
    return render(request,'student_feedback_app/lecturer_home.html',context_dict)

def my_provided_feedback(request):
    context_dict = {}
    if request.user.is_lecturer:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        fb = lect.feedback_set.all()
        context_dict['lect'] = lect
        context_dict['feedback'] = fb
    else:
        return HttpResponse("you are not allowed here")

    return render(request,'student_feedback_app/my_provided_feedback.html',context_dict)

def lecturer_class(request,subject_slug):
    context_dict = {}
    if request.user.is_lecturer:
        try:
            cla = Class.objects.get(subject_slug=subject_slug)
            lect = cla.lecturer
            students = cla.students.all()
            top_students = students.order_by('-score')
            context_dict['class'] = cla
            context_dict['lect'] = lect
            context_dict['students'] = students
            # Add top students for each class. This requires editing models to store class in feedback
            fb = cla.feedback_set.all().order_by('-date_given')
            context_dict['feedback'] = fb
        except:
            context_dict['class'] = None
            context_dict['lect'] = None
            context_dict['students'] = None
            context_dict['feedback'] = None
            return HttpResponse("class does not exist")
    else:
        return HttpResponse("you are not allowed here")

    return render(request,'student_feedback_app/lecturer_class.html',context_dict)


def lecturer_view_student(request,student_number):
    context_dict = {}
    if request.user.is_lecturer:
        try:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            stud_user = User.objects.get(id_number=student_number)
            stud = StudentProfile.objects.get(student=stud_user)
            fb = stud.feedback_set.all()
            classes = stud.classes.all()
            context_dict['lecturer'] = lect
            context_dict['student'] = stud
            context_dict['feedback'] = fb
            context_dict['classes'] = classes
        except:
            return HttpResponse("Student does not exist")
    else:
        return HttpResponse("You are not allowed here")
    return render(request,'student_feedback_app/lecturer_view_student.html',context_dict)

def add_feedback(request,subject_slug,student_number):
    if not request.user.is_lecturer:
        return HttpResponse("you are not allowed here")
    context_dict = {}
    try:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        stud_user = User.objects.get(id_number=student_number)
        stud = StudentProfile.objects.get(student=stud_user)
        fb = stud.feedback_set.all()
        context_dict['lecturer'] = lect
        context_dict['student'] = stud
        context_dict['feedback'] = fb
        cla = Class.objects.get(subject_slug=subject_slug)
        context_dict['class'] = cla

        context = RequestContext(request)
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                new_fb = form.save(commit=False)
                new_fb.student = stud
                stud.score += new_fb.points
                new_fb.lecturer = lect
                new_fb.which_class = cla
                new_fb.date_given = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                stud.save()
                new_fb.save()
                return my_provided_feedback(request)
            else:
                print(form.errors)
        else:
            form = FeedbackForm()
        context_dict['form'] = form
        return render(request,'student_feedback_app/add_feedback.html',context_dict)
    except:
        context_dict['student'] = None
        context_dict['feedback'] = None
        return HttpResponse("Couldn't find the student")
    return render(request,'student_feedback_app/add_feedback.html',context_dict)

def lecturer_all_classes(request):
    context_dict = {}
    if request.user.is_lecturer:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        classes = lect.class_set.all()
        fb = lect.feedback_set.all()
        context_dict['lect'] = lect
        context_dict['classes'] = classes
        context_dict['feedback'] = fb
    else:
        return HttpResponse("You are not allowed here")

    return render(request,'student_feedback_app/lecturer_classes.html',context_dict)

def create_class(request):

    context_dict = {}
    if not request.user.is_lecturer:
        return HttpResponse("You are not allowed here")


    try:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        context_dict["lecturer"] = lect

        if request.method == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                newClass = form.save(commit=False)
                newClass.lecturer = lect
                newClass.save()
                return lecturer_all_classes(request)

            else:

                print(form.errors)

        else:
            form = ClassForm()

        context_dict["form"] = form
        return render(request, 'student_feedback_app/create_class.html', context_dict)
    except:
        return HttpResponse("something went wrong")

class FeedbackList(generics.ListAPIView):
    queryset = Feedback.objects.all().order_by('points')
    serializer_class = FeedbackSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Feedback_with_categoryList(generics.ListAPIView):
    queryset = Feedback_with_category.objects.all()
    serializer_class = Feedback_with_categorySerializer

class Feedback_with_studentList(generics.ListAPIView):
    queryset = Feedback_with_student.objects.all()
    serializer_class = Feedback_with_studentSerializer


