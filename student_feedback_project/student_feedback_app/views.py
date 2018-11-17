from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import LecturerProfile,Feedback,Course,StudentProfile,User
from .forms import CourseForm,FeedbackForm
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

# Create your views here.
def index(request):
    return HttpResponse("This is the homepage")



def student_home(request):
    context_dict={}
    if request.user.is_authenticated and request.user.is_student:
        try:
            stud = StudentProfile.objects.get(student=request.user)
            fb = stud.feedback_set.all().order_by('-datetime_given')
            courses=stud.course_set.all()
            context_dict['student'] = stud
            context_dict['courses'] = courses
            context_dict['feedback'] = fb
        except:
            context_dict['error'] = "error"
            return  render(request, 'student_feedback_app/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/error_page.html', context_dict)
    return render(request, 'student_feedback_app/student_home.html', context_dict)




def all_feedback(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_student:
        stud= StudentProfile.objects.get(student=request.user)
        fb = stud.feedback_set.all()
        context_dict['stud'] = stud
        context_dict['feedback'] = fb
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)

    return render(request,'student_feedback_app/all_feedback.html',context_dict)


def student_all_courses(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_student:
        stud = StudentProfile.objects.get(student=request.user)
        courses = stud.course_set.all()
        fb = stud.feedback_set.all()
        context_dict['stud'] = stud
        context_dict['courses'] = courses
        context_dict['feedback'] = fb
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)
    return render(request,'student_feedback_app/student_courses.html',context_dict)


def student_course(request, subject_slug):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_student:
        try:
            course = Course.objects.get(subject_slug=subject_slug)
            stud = StudentProfile.objects.get(student=request.user)
            print(stud.score)
            lect = course.lecturer
            students = course.students.all()
            top_students = students.order_by('-score')
            context_dict['course'] = course
            context_dict['lect'] = lect
            context_dict['students'] = students
            # Add top students for each course. This requires editing models to store course in feedback
            fb = course.feedback_set.all().order_by('-datetime_given')
            context_dict['feedback'] = fb
        except:
            context_dict['course'] = None
            context_dict['lect'] = None
            context_dict['students'] = None
            context_dict['feedback'] = None
            context_dict['error'] = "no_course"
            return render(request, 'student_feedback_app/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/error_page.html', context_dict)

    return render(request, 'student_feedback_app/student_course.html', context_dict)





def lecturer_home(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        try:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            fb = lect.feedback_set.all().order_by('-datetime_given')
            courses = lect.course_set.all()
            context_dict['lecturer'] = lect
            context_dict['courses'] = courses
            context_dict['feedback'] = fb
        except:
            context_dict['error'] = "error"
            return render(request,'student_feedback_app/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)
    return render(request,'student_feedback_app/lecturer_home.html',context_dict)

def my_provided_feedback(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        fb = lect.feedback_set.all()
        context_dict['lect'] = lect
        context_dict['feedback'] = fb
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)

    return render(request,'student_feedback_app/my_provided_feedback.html',context_dict)

def lecturer_course(request,subject_slug):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        try:
            course = Course.objects.get(subject_slug=subject_slug)
            lect = course.lecturer
            students = course.students.all()
            top_students = students.order_by('-score')
            context_dict['course'] = course
            context_dict['lect'] = lect
            context_dict['students'] = students
            # Add top students for each course. This requires editing models to store course in feedback
            fb = course.feedback_set.all().order_by('-datetime_given')
            context_dict['feedback'] = fb
        except:
            context_dict['course'] = None
            context_dict['lect'] = None
            context_dict['students'] = None
            context_dict['feedback'] = None
            context_dict['error'] = "no_course"
            return render(request,'student_feedback_app/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)

    return render(request,'student_feedback_app/lecturer_course.html',context_dict)


def lecturer_view_student(request,student_number):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        try:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            stud_user = User.objects.get(id_number=student_number)
            stud = StudentProfile.objects.get(student=stud_user)
            fb = stud.feedback_set.all()
            courses = stud.courses.all()
            context_dict['lecturer'] = lect
            context_dict['student'] = stud
            context_dict['feedback'] = fb
            context_dict['courses'] = courses
        except:
            context_dict['error'] = "no_student"
            return render(request,'student_feedback_app/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)
    return render(request,'student_feedback_app/lecturer_view_student.html',context_dict)

def add_feedback(request,subject_slug,student_number):
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)
    context_dict = {}
    try:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        stud_user = User.objects.get(id_number=student_number)
        stud = StudentProfile.objects.get(student=stud_user)
        fb = stud.feedback_set.all()
        context_dict['lecturer'] = lect
        context_dict['student'] = stud
        context_dict['feedback'] = fb
        course = Course.objects.get(subject_slug=subject_slug)
        context_dict['course'] = course

        context = RequestContext(request)
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                new_fb = form.save(commit=False)
                new_fb.student = stud
                stud.score += new_fb.points
                new_fb.lecturer = lect
                new_fb.which_course = course
                new_fb.datetime_given = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        context_dict['error'] = "no_student"
        return render(request,'student_feedback_app/error_page.html', context_dict)
    return render(request,'student_feedback_app/add_feedback.html',context_dict)

def lecturer_all_courses(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        courses = lect.course_set.all()
        fb = lect.feedback_set.all()
        context_dict['lect'] = lect
        context_dict['courses'] = courses
        context_dict['feedback'] = fb
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)

    return render(request,'student_feedback_app/lecturer_courses.html',context_dict)

def create_course(request):

    contextDict = {}
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/error_page.html', context_dict)


    try:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        contextDict["lecturer"] = lect

        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                newCourse = form.save(commit=False)
                newCourse.lecturer = lect
                newCourse.save()
                return lecturer_all_courses(request)

            else:

                print(form.errors)

        else:
            form = CourseForm()

        contextDict["form"] = form
        return render(request, 'student_feedback_app/create_course.html', contextDict)


    except:
        context_dict['error'] = "error"
        return render(request,'student_feedback_app/error_page.html', context_dict)
