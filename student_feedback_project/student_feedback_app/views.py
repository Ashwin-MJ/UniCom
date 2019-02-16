from django import http
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth import login
from django.core import serializers

from student_feedback_app.forms import *
from student_feedback_app.models import *
from student_feedback_app.serializers import *

from rest_framework import generics
from dal import autocomplete
import datetime
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


def index(request):
    return HttpResponseRedirect('/accounts/login/')

def my_profile(request):
    context_dict = {}
    if request.user.is_authenticated:
        if request.user.is_student:
            try:
                stud = StudentProfile.objects.get(student=request.user)
                fb = stud.feedback_set.all().order_by('-datetime_given')
                context_dict['student'] = stud
                context_dict['courses'] = stud.get_courses_with_score()
                context_dict['feedback'] = fb
            except:
                context_dict['error'] = "error"
                return render(request, 'student_feedback_app/general/error_page.html', context_dict)
        elif request.user.is_lecturer:
            try:
                lect = LecturerProfile.objects.get(lecturer=request.user)
                fb = request.user.feedback_set.all().order_by('-datetime_given')
                context_dict['lecturer'] = lect
                context_dict['courses'] = lect.get_courses_with_students()
                context_dict['feedback'] = fb
            except:
                context_dict['error'] = "error"
                return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    else:
        # User not authenticated error
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    return render(request, 'student_feedback_app/general/my_profile.html', context_dict)

def edit_bio(request):
    context_dict={}
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                user = request.user
                form = EditBioForm(request.POST)
                if form.is_valid():
                    new_bio=form.cleaned_data["bio"]
                    new_degree=form.cleaned_data["degree"]
                    user.degree=new_degree
                    user.bio= new_bio
                    user.save()
                    return my_profile(request)
                else:
                    print(form.errors)
            else:
                form = EditBioForm()
            context_dict["form"] = form
            return render(request, 'student_feedback_app/general/edit_bio.html', context_dict)
        except:
            context_dict['error'] = "error"
            return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/general/error_page.html', context_dict, )

def student_home(request):
    context_dict={}
    fbCat = {}
    catColours = {}
    if request.user.is_authenticated and request.user.is_student:
        try:
            stud = StudentProfile.objects.get(student=request.user)
            fb = stud.feedback_set.all().order_by('-datetime_given')
            courses=stud.courses.all()
            for feedback in fb:
                cat = feedback.category.name
                if cat not in fbCat:
                    fbCat[cat] = [[feedback.points, feedback.datetime_given.strftime('%Y-%m-%d %H:%M')]]
                    catColours[cat] = [feedback.category.colour]
                else:
                    fbCat[cat].append([feedback.points, feedback.datetime_given.strftime('%Y-%m-%d %H:%M')])
            context_dict['student'] = stud
            context_dict['courses'] = courses
            context_dict['feedback'] = fb
            context_dict['feedbackData'] = json.dumps(fbCat)
            context_dict['catColours'] = json.dumps(catColours)

        except:
            context_dict['error'] = "error"
            return  render(request, 'student_feedback_app/general/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    return render(request, 'student_feedback_app/student/student_home.html', context_dict)

def student_all_feedback(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_student:
        stud= StudentProfile.objects.get(student=request.user)
        fb = stud.feedback_set.all().order_by('-datetime_given')
        context_dict['student'] = stud
        context_dict['feedback'] = fb
        top_attributes = stud.get_top_attributes()
        if len(top_attributes) > 4:
            top_attributes =  top_attributes[:4]
        context_dict['top_attributes'] = top_attributes
        context_dict['to_improve'] = stud.get_weaknesses()
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    return render(request,'student_feedback_app/student/student_all_feedback.html',context_dict)


def student_courses(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_student:
        stud = StudentProfile.objects.get(student=request.user)
        courses = stud.courses.all()
        fb = stud.feedback_set.all()
        context_dict['stud'] = stud
        context_dict['courses'] = stud.get_courses_with_score()
        context_dict['feedback'] = fb
        if(request.method == 'POST'):
            form = AddCourseForm(request.POST)
            stud = StudentProfile.objects.get(student = request.user)
            if(form.is_valid()):
                try:
                    course = Course.objects.get(course_token=form.cleaned_data["course_token"] )
                    stud.courses.add(course)
                    course.students.add(stud)
                    stud.save()
                    course.save()
                    return student_home(request)
                except:
                    context_dict['error'] = "no_course"
                    return render(request, 'student_feedback_app/general/error_page.html', context_dict)
            else:
                print(form.errors)
        else:
            form = AddCourseForm()
        context_dict["form"] = form
        return render(request, 'student_feedback_app/student/student_courses.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def student_course(request, subject_slug):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_student:
        try:
            course = Course.objects.get(subject_slug=subject_slug)
            stud = StudentProfile.objects.get(student=request.user)
            lecturers = course.lecturers
            students = course.students.all()
            top_students = students.order_by('-score')
            context_dict['course'] = course
            context_dict['lecturers'] = lecturers
            # lect = course.lecturer.all()
            # context_dict['lect'] = lect[0]
            context_dict['students'] = students
            context_dict['sorted_students'] = course.get_leaderboard()
            context_dict['feedback'] = stud.get_fb_for_course(course.subject)
            context_dict['score'] = stud.get_score_for_course(course.subject)
            context_dict['student'] = stud
        except:
            context_dict['course'] = None
            context_dict['lect'] = None
            context_dict['students'] = None
            context_dict['feedback'] = None
            context_dict['error'] = "no_course"
            return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    return render(request, 'student_feedback_app/student/student_course.html', context_dict)

def student_add_individual_feedback(request,subject_slug,student_number):
    if not request.user.is_authenticated or not request.user.is_student:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    context_dict = {}
    try:
        from_stud = StudentProfile.objects.get(student=request.user)
        stud_user = User.objects.get(id_number=student_number)
        stud = StudentProfile.objects.get(student=stud_user)

        fb = stud.feedback_set.all()
        context_dict['from_student'] = from_stud
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
                new_fb.from_user = request.user
                new_fb.which_course = course
                new_fb.datetime_given = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                stud.save()
                new_fb.pk = None
                new_fb.save()
                return student_home(request)
            else:
                print(form.errors)
        else:
            form = FeedbackForm()
        context_dict['form'] = form
        return render(request,'student_feedback_app/student/student_add_individual_feedback.html',context_dict)
    except:
        context_dict['student'] = None
        context_dict['feedback'] = None
        context_dict['error'] = "no_student"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def my_provided_feedback(request):
    context_dict = {}
    if not request.user.is_authenticated:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    try:
        if request.user.is_student:
            stud = StudentProfile.objects.get(student=request.user)
            fb = request.user.feedback_set.all().order_by('-datetime_given')
            context_dict['student'] = stud
            context_dict['feedback'] = fb
            return render(request,'student_feedback_app/student/student_provided_feedback.html',context_dict)
        if request.user.is_lecturer:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            fb = request.user.feedback_set.all().order_by('-datetime_given')
            context_dict['lecturer'] = lect
            context_dict['feedback'] = fb
            return render(request,'student_feedback_app/lecturer/lecturer_provided_feedback.html',context_dict)
    except:
        context_dict['error'] = "error"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def lecturer_home(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        try:
            lect = LecturerProfile.objects.get(lecturer=request.user)
            fb = request.user.feedback_set.all().order_by('-datetime_given')
            courses = lect.course_set.all()
            context_dict['lecturer'] = lect
            context_dict['courses'] = courses
            context_dict['feedback'] = fb
        except:
            context_dict['error'] = "error"
            return render(request,'student_feedback_app/general/error_page.html', context_dict)
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('student_home')
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    return render(request,'student_feedback_app/lecturer/lecturer_home.html',context_dict)

def lecturer_course(request,subject_slug):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        try:
            course = Course.objects.get(subject_slug=subject_slug)
            lect = LecturerProfile.objects.get(lecturer=request.user)
            students = course.students.all()
            context_dict['course'] = course
            context_dict['lecturer'] = lect
            context_dict['students_with_score'] = {}
            # Add top students for each course. This requires editing models to store course in feedback
            fb = course.feedback_set.all().order_by('-datetime_given')
            students = course.get_students_with_score()
            context_dict['students_with_score'] = [(k, students[k]) for k in sorted(students)]
            context_dict['sorted_students'] = course.get_leaderboard()
            context_dict['feedback'] = fb
        except:
            context_dict['error'] = "no_course"
            return render(request,'student_feedback_app/general/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    return render(request,'student_feedback_app/lecturer/lecturer_course.html',context_dict)

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
            context_dict['courses'] = stud.get_courses_with_score()
        except:
            context_dict['error'] = "no_student"
            return render(request,'student_feedback_app/general/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    return render(request,'student_feedback_app/lecturer/lecturer_view_student.html',context_dict)

def lecturer_add_individual_feedback(request,subject_slug,student_number):
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    context_dict = {}
    try:
        # Retrieving student string from cookies
        students_string = request.COOKIES.get("indiv_students")
        try:
            students_list = json.loads(students_string)
        except:
            # Seems to be an error in using json.loads for a list with a single element so do this instead
            students_list = students_string
        # At this point, the variable students_list contains a list of all students still to be given feedback
        # Remove current student from that list
        # Removing first element of list (current student)
        students_list = students_list[1:]
        # Saving the above updated list as a cookie 'indiv_students'
        request.COOKIES["indiv_students"] = students_list
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
                new_fb.from_user = request.user
                new_fb.which_course = course
                new_fb.datetime_given = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                stud.save()
                new_fb.pk = None
                new_fb.save()
                rem_students = students_list
                # Check if there are more students to provide individual fb to
                if(len(rem_students) >= 1):
                    next_stud = rem_students[0]
                    # Get response as url for next student
                    response = HttpResponseRedirect(reverse('lect_add_individual_feedback', args=[course.subject_slug, next_stud]))
                    # Set the cookie in the response so that the next page has the updated cookie
                    # i.e the updated list of students
                    response.set_cookie("indiv_students",json.dumps(rem_students))
                    return response
                else:
                    # Delete cookies so there are no issues the next time group/individual feedback is given
                    request.COOKIES["indiv_students"] = ""
                    request.COOKIES['students'] = ""
                    response = my_provided_feedback(request)
                    response.delete_cookie('indiv_students')
                    return response
            else:
                print(form.errors)
        else:
            form = FeedbackForm()
        context_dict['form'] = form
        return render(request,'student_feedback_app/lecturer/lecturer_add_individual_feedback.html',context_dict)
    except:
        context_dict['student'] = None
        context_dict['feedback'] = None
        context_dict['error'] = "no_student"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def add_group_feedback(request,subject_slug):
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    context_dict = {}
    try:
        students_string = request.COOKIES.get("students")
        students_list = json.loads(students_string)
        stud_profiles = []
        for student_id in students_list:
            stud_user = User.objects.get(id_number=student_id)
            stud_profiles.append(StudentProfile.objects.get(student=stud_user))
        context_dict['students'] = stud_profiles
        lect = LecturerProfile.objects.get(lecturer=request.user)
        context_dict['lecturer'] = lect
        course = Course.objects.get(subject_slug=subject_slug)
        context_dict['subject'] = course
        context = RequestContext(request)
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                for student in stud_profiles:
                    new_fb = form.save(commit=False)
                    created_fb = Feedback(student=student)
                    created_fb.pre_defined_message = new_fb.pre_defined_message
                    created_fb.pre_defined_message.category = Category.objects.get(name=new_fb.category)
                    created_fb.pre_defined_message.save()
                    created_fb.category = created_fb.pre_defined_message.category
                    student.score += new_fb.points
                    created_fb.from_user = request.user
                    created_fb.which_course = course
                    created_fb.points = new_fb.points
                    created_fb.optional_message = new_fb.optional_message
                    created_fb.datetime_given = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    student.save()
                    created_fb.pk = None
                    created_fb.save()
            else:
                print(form.errors)
            request.COOKIES["students"] = ""
            return my_provided_feedback(request)
        else:
            form = FeedbackForm()
        context_dict['form'] = form

        return render(request,'student_feedback_app/lecturer/lecturer_add_group_feedback.html',context_dict)

    except:
        context_dict['error'] = "error"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def lecturer_courses(request):
    context_dict = {}
    if request.user.is_authenticated and request.user.is_lecturer:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        courses = lect.courses.all()
        fb = request.user.feedback_set.all().order_by('-datetime_given')
        top_students = lect.get_my_students().order_by('-score')[:5]
        context_dict['lecturer'] = lect
        context_dict['courses'] = courses
        context_dict['feedback'] = fb
        context_dict['top_students'] = top_students
        if(request.method == 'POST'):
            form = AddCourseForm(request.POST)
            lect = LecturerProfile.objects.get(lecturer = request.user)
            if(form.is_valid()):
                try:
                    course = Course.objects.get(course_token=form.cleaned_data["course_token"] )
                    lect.courses.add(course)
                    course.lecturers.add(lect)
                    lect.save()
                    course.save()
                    return lecturer_home(request)
                except:
                    context_dict['error'] = "no_course"
                    return render(request, 'student_feedback_app/general/error_page.html', context_dict)
            else:
                print(form.errors)
        else:
            form = AddCourseForm()
        context_dict["form"] = form
        return render(request, 'student_feedback_app/lecturer/lecturer_courses.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def customise_options(request):
    context_dict = {}
    if not request.user.is_authenticated:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    try:
        context_dict['categories'] = request.user.category_set.all()
        messages = request.user.message_set.all()

        form = EditCategoryForm()
        context_dict["form"] = form

        all_messages = {}
        for message in messages:
            all_messages[message.id] = message.text

        context_dict['messages'] = json.dumps(all_messages)
        context_dict['messages_qs'] = messages
        return render(request, 'student_feedback_app/general/customise_options.html', context_dict)
    except:
        context_dict['error'] = "error"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def create_course(request):
    context_dict = {}
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    try:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        context_dict["lecturer"] = lect
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                newCourse = form.save(commit=False)
                newCourse.lecturers.add(lect)
                newCourse.save()
                return lecturer_courses(request)
            else:
                print(form.errors)
        else:
            form = CourseForm()
        context_dict["form"] = form
        return render(request, 'student_feedback_app/lecturer/lecturer_create_course.html', context_dict)
    except:
        context_dict['error'] = "error"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

class FeedbackDetail(APIView):
    """
    Retrieve or delete a Feedback instance.
    """
    def get_object(self, fb_id):
        try:
            return Feedback.objects.get(feedback_id=fb_id)
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, fb_id, format=None):
        fb = self.get_object(fb_id)
        serializer = FeedbackSerializer(fb)
        return Response(serializer.data)

    def delete(self, request, fb_id, format=None):
        fb = self.get_object(fb_id)
        fb.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryDetail(APIView):
    """
    Retrieve, update or delete a Category instance.
    Can add a new method to create a new Category instance
    """
    def get_object(self, cat_id):
        try:
            return Category.objects.get(id=cat_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, cat_id, format=None):
        cat = self.get_object(cat_id)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    def delete(self, request, cat_id, format=None):
        cat = self.get_object(cat_id)
        messages = cat.message_set.all()
        for mess in messages:
            mess.delete()
        request.user.category_set.remove(cat)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, cat_id, format=None):
        cat = self.get_object(cat_id)
        cat.name = request.data.get('name')
        cat.colour = request.data.get('colour')
        cat.save()
        return Response(status=status.HTTP_200_OK)

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()
        query_set = self.request.user.category_set.all()
        category = self.forwarded.get('category', None)
        if self.q:
            query_set = query_set.filter(name__istartswith=self.q)
            return query_set
        if category:
            query_set = Message.objects.filter(user=self.request.user,category=category)
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
        if self.request.user.is_authenticated:
            return True
        else:
            return False


class FeedbackSortedByPoints(generics.ListAPIView):
    queryset = Feedback_with_course.objects.all().order_by('-points')
    serializer_class = Feedback_with_courseSerializer

class FeedbackSortedByDate(generics.ListAPIView):
    queryset = Feedback_with_course.objects.all().order_by('-datetime_given')
    serializer_class = Feedback_with_courseSerializer

class FeedbackSortedByCourse(generics.ListAPIView):
    queryset = Feedback_with_course.objects.all().order_by('courseName')
    serializer_class = Feedback_with_courseSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Feedback_with_categoryList(generics.ListAPIView):
    queryset = Feedback_with_category.objects.all()
    serializer_class = Feedback_with_categorySerializer

class Feedback_with_studentList(generics.ListAPIView):
    queryset = Feedback_with_student.objects.all()
    serializer_class = Feedback_with_studentSerializer

class Feedback_with_from_userList(generics.ListAPIView):
    queryset = Feedback_with_from_user.objects.all()
    serializer_class = Feedback_with_from_userSerializer

class MessageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Message.objects.none()
        query_set = self.request.user.message_set.all()
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
        if self.request.user.is_authenticated:
            return True
        else:
            return False

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_lecturer:
                return redirect('lecturer_home')
            else:
                return redirect('student_home')
    else:
        form = RegisterForm()
    return render(request, 'registration/registration_form.html', {'form': form})
