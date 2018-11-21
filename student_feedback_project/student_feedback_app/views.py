from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import LecturerProfile,Feedback,Course,StudentProfile,User,Category,Message
from .forms import CourseForm,FeedbackForm, addCourseForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from dal import autocomplete
import datetime
from django import http

# Create your views here.
def index(request):
    return render(request, 'student_feedback_app/index.html')

def student_home(request):
    context_dict={}
    if request.user.is_authenticated and request.user.is_student:
        try:
            stud = StudentProfile.objects.get(student=request.user)
            fb = stud.feedback_set.all().order_by('-datetime_given')
            courses=stud.courses.all()
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




def student_all_feedback(request):
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
        courses = stud.courses.all()
        fb = stud.feedback_set.all()
        context_dict['stud'] = stud
        context_dict['courses'] = courses
        context_dict['feedback'] = fb
        if(request.method == 'POST'):
            form = addCourseForm(request.POST)
            stud = StudentProfile.objects.get(student = request.user)
            if(form.is_valid()):
                try:
                    course = Course.objects.get(course_token=form.cleaned_data["course_token"] )
                    stud.courses.add(course)
                    stud.save()
                    return student_home(request)
                except:
                    context_dict['error'] = "no_course"
                    return render(request, 'student_feedback_app/error_page.html', context_dict)
            else:
                print(form.errors)
        else:
            form = addCourseForm()
        context_dict["form"] = form
        return render(request, 'student_feedback_app/student_courses.html', context_dict)
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
                new_fb.pre_defined_message.category = Category.objects.get(name=new_fb.category)
                new_fb.pre_defined_message.save()
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

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated or not self.request.user.is_lecturer:
            return Category.objects.none()

        query_set = Category.objects.all()

        category = self.forwarded.get('category', None)

        if self.q:
            query_set = query_set.filter(name__istartswith=self.q)
            return query_set

        if category:
            query_set = Message.objects.filter(category=category)

        return query_set

    def get_create_option(self,context,q):
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            create_option = [{
                'id': q,
                'text': ('Create a new category: "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option

    def has_add_permission(self, request):
        if self.request.user.is_authenticated and self.request.user.is_lecturer:
            return True
        else:
            return False

class MessageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated or not self.request.user.is_lecturer:
            return Message.objects.none()

        query_set = Message.objects.all()

        category = self.forwarded.get('category', None)

        if category:
            query_set = Message.objects.filter(category=category)

        return query_set

    def get_create_option(self,context,q):
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            category = self.forwarded.get('category',None)
            cat = Category.objects.get(name=category)

            create_option = [{
                'id': q,
                'text': ('Create a new message: "%(new_value)s"') % {'new_value': q},
                'category': category,
                'create_id': True,
            }]

        return create_option

    def render_to_response(self, context):
        q = self.request.GET.get('q', None)

        create_option = self.get_create_option(context, q)

        return http.JsonResponse(
            {
                'results': self.get_results(context) + create_option,
                'pagination': {
                    'more': self.has_more(context)
                }
            })

    def has_add_permission(self, request):
        if self.request.user.is_authenticated and self.request.user.is_lecturer:
            return True
        else:
            return False
