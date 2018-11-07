from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .models import Class, LecturerProfile

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
    return HttpResponse("This page shows all of the feedback I have given to students")


def lecturer_class(request):
    return HttpResponse("This page is to view a class from a Lecturer's prespective")


def lecturer_view_student(request):
    return HttpResponse("This page is to view a student's page from a Lecturer's perspective")


def add_feedback(request):
    return HttpResponse("This page is to add feedback")


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


# def class_created(request):
#     form = classForm()
#     if request.method == 'POST':
#         form = classForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return index(request)
#         else:
#             print(form.errors)
#     return render(request, 'student_feedback_app/class_created.html', {'form':form})
