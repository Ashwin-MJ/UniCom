from django.shortcuts import render
from django.http import HttpResponse
from .models import LecturerProfile,Feedback,Class,StudentProfile,User
from .forms import *

# Create your views here.
def index(request):
    return HttpResponse("This is the homepage")


def login(request):
    return HttpResponse("This is the login/sign up page")


def student_home(request):
    return render(request, 'student_feedback_app/student_home.html')

def all_feedback(request):
    return HttpResponse("This page shows all of my feedback")


def my_classes(request):
    return HttpResponse("This page shows all of my classes")


def lecturer_home(request):
    return HttpResponse("This is the homepage for Lecturer")

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
            fb = cla.feedback_set.all().order_by('-datetime')
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


def lecturer_view_student(request):
    return HttpResponse("This page is to view a student's page from a Lecturer's perspective")

def add_feedback(request,student_number):
    context_dict = {}
    if request.user.is_lecturer:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        try:
            stud_user = User.objects.get(id_number=student_number)
            stud = StudentProfile.objects.get(student=stud_user)
            fb = stud.feedback_set.all()
            context_dict['student'] = stud
            context_dict['feedback'] = fb
        except:
            context_dict['student'] = None
            context_dict['feedback'] = None
            return HttpResponse("Couldn't find the student")
    else:
        return HttpResponse("you are not allowed here")

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
    if request.user.is_lecturer:
        form = classForm()
        if request.method == 'POST':
            form = classForm(request.POST)
            if form.is_valid():
                if request.POST.get("create_class"):
                    lecturer = LecturerProfile.objects.get(lecturer=request.user)
                    subject = Class.objects.get_or_create(class_name=form.cleaned_data["class_name"],
                                                          class_description=form.cleaned_data["class_description"],
                                                          lecturer=lecturer)
                    #LecturerProfile.Classes.add(subject)
                form.save(commit=True)
                return index(request)
            else:
                print(form.errors)
    else:
        return HttpResponse("You are not allowed here")

    return render(request, 'student_feedback_app/create_class.html', {'form':form})
