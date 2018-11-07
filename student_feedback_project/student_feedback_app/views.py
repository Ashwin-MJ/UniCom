from django.shortcuts import render
from django.http import HttpResponse
from student_feedback_app.models import Feedback
from datetime import datetime, timedelta
from django.utils import timezone
from .models import LecturerProfile,Feedback,Class,StudentProfile
from .forms import *


# Create your views here.
def index(request):
    return HttpResponse("This is the homepage")


def login(request):
    return HttpResponse("This is the login/sign up page")


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
    return HttpResponse("This is the homepage for Lecturer")

def my_provided_feedback(request,lecturer_number):
    context_dict = {}
    try:
        lect = LecturerProfile.objects.get(lecturer_number=lecturer_number)
        fb = lect.feedback_set.all()
        context_dict['lect'] = lect
        context_dict['feedback'] = fb
    except:
        context_dict['lect'] = None
        context_dict['feedback'] = None

    return render(request,'student_feedback_app/my_provided_feedback.html',context_dict)

def lecturer_class(request,subject_slug):
    context_dict = {}
    try:
        cla = Class.objects.get(subject_slug=subject_slug)
        lect = cla.lecturer
        students = cla.students.all()
        top_students = students.order_by('-score')
        context_dict['class'] = cla
        context_dict['lect'] = lect
        context_dict['students'] = students
        # Add top students for each class. This requires editing models to store class in feedback
        fb = cla.feedback_set.all().order_by('-datetime')
        context_dict['feedback'] = fb
    except:
        context_dict['class'] = None
        context_dict['lect'] = None
        context_dict['students'] = None
        context_dict['feedback'] = None

    return render(request,'student_feedback_app/lecturer_class.html',context_dict)



def lecturer_view_student(request):
    return HttpResponse("This page is to view a student's page from a Lecturer's perspective")

def add_feedback(request,student_slug):
    context_dict = {}
    print(student_slug)
    try:
        stud = StudentProfile.objects.get(student_slug=student_slug)
        fb = stud.feedback_set.all()
        context_dict['student'] = stud
        context_dict['feedback'] = fb
    except:
        context_dict['student'] = None
        context_dict['feedback'] = None
    return render(request,'student_feedback_app/add_feedback.html',context_dict)

def lecturer_all_classes(request,lecturer_number):
    context_dict = {}
    try:
        lect = LecturerProfile.objects.get(lecturer_number=lecturer_number)
        classes = lect.class_set.all()
        fb = lect.feedback_set.all()
        context_dict['lect'] = lect
        context_dict['classes'] = classes
        context_dict['feedback'] = fb
    except:
        context_dict['lect'] = None
        context_dict['classes'] = None
        context_dict['feedback'] = None

    return render(request,'student_feedback_app/lecturer_classes.html',context_dict)

def create_class(request):
    form = classForm()
    if request.method == 'POST':
        form = classForm(request.POST)
        if form.is_valid():
            if request.POST.get("create_class"):
                subject = Class.objects.get_or_create(class_name=form.cleaned_data["class_name"],
                                                      class_description=form.cleaned_data["class_description"])
                LecturerProfile.Classes.add(subject)


            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'student_feedback_app/create_class.html', {'form': form})


