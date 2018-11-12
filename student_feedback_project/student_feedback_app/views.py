from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import LecturerProfile,Feedback,Class,StudentProfile,User
from .forms import classForm,FeedbackForm
from django.shortcuts import render_to_response
from django.template import RequestContext

import datetime

# Create your views here.
def index(request):
    return HttpResponse("This is the homepage")

def student_home(request):
    return render(request, 'student_feedback_app/student_home.html')

def all_feedback(request):
    return HttpResponse("This page shows all of my feedback")


def my_classes(request):
    return HttpResponse("This page shows all of my classes")

def lecturer_home(request):
    context_dict = {}
    if request.user.is_lecturer:
        try:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            fb = lect.feedback_set.all().order_by('-datetime')
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
                new_fb.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
