from django.shortcuts import render
from django.http import HttpResponse

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

def lecturer_all_classes(request):
    return HttpResponse("This is for a lecturer to view all his classes")

def create_class(request):
    return HttpResponse("This is to create a class")
