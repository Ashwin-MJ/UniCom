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

from ast import literal_eval
from populate import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


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

def view_profile(request,student_number):
    context_dict = {}
    if request.user.is_authenticated:
        if request.user.is_student:
            # Case 1 - Student view another Student
            ## The student should only see feedback given by themself
            try:
                stud_user = User.objects.get(id_number=student_number)
                stud = StudentProfile.objects.get(student=stud_user)
                fb = stud.feedback_set.all().filter(from_user=request.user).order_by('-datetime_given')
                context_dict['student'] = stud
                context_dict['courses'] = stud.get_courses_with_score()
                context_dict['feedback'] = fb
            except:
                context_dict['error'] = "error"
                return render(request, 'student_feedback_app/general/error_page.html', context_dict)
        elif request.user.is_lecturer:
            # Case 2 - Lecturer view Student
            ## The lecturer should be able to see all feedback given to the student
            try:
                lect = LecturerProfile.objects.get(lecturer=request.user)
                stud_user = User.objects.get(id_number=student_number)
                stud = StudentProfile.objects.get(student=stud_user)
                fb = stud.feedback_set.all().order_by('-datetime_given')
                context_dict['student'] = stud
                context_dict['courses'] = stud.get_courses_with_score()
                context_dict['feedback'] = fb
            except:
                context_dict['error'] = "error"
                return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    else:
        context_dict['error'] = "auth"
        return render(request, 'student_feedback_app/general/error_page.html', context_dict)
    return render(request, 'student_feedback_app/general/view_profile.html', context_dict)


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
    achievs = {}
    if request.user.is_authenticated and request.user.is_student:
        try:
            stud = StudentProfile.objects.get(student=request.user)
            fb = stud.feedback_set.all().order_by('-datetime_given')
            courses = stud.courses.all()
            for feedback in fb:
                cat = feedback.category.name
                if cat not in fbCat:
                    fbCat[cat] = [[feedback.points, feedback.datetime_given.strftime('%Y-%m-%d %H:%M')]]
                    try:
                        stud_cat = Category.objects.get(name=feedback.category.name,user=request.user)
                        catColours[cat] = [stud_cat.colour]
                    except:
                        catColours[cat] = [feedback.category.colour]
                else:
                    fbCat[cat].append([feedback.points, feedback.datetime_given.strftime('%Y-%m-%d %H:%M')])
            stud.achievement_set.all().delete()
            scores = stud.get_score_for_category()

            for attribute in scores:
                achievM = Achievement(student=stud)
                try:
                    achievM.gen_achievement(attribute, scores[attribute],request.user)
                    achievM.save()
                except:
                    ## TODO: Figure out how to handle this error
                    print("Doesn't exit")

            stud.achievement_set.all()
            for achvm in stud.achievement_set.all():
                achvm.achiev = literal_eval(achvm.achiev)
                for val in achvm.achiev:
                    if achvm.category in achievs:
                        achievs[achvm.category].append(val)
                    else:
                        achievs[achvm.category] = [val]
                achievs[achvm.category].sort()


            # The follow dictionary is required to ensure the colour displayed for a given feedback
            # corresponds to the student's colour of that category and NOT the lecturers
            fb_with_colour = {}
            stud_cats = request.user.category_set.all()

            for feedback in fb:
                try:
                    stud_cat = Category.objects.get(name=feedback.category.name,user=request.user)
                    fb_with_colour[feedback] = stud_cat.colour
                except:
                    fb_with_colour[feedback] = feedback.category.colour

            context_dict['student'] = stud
            context_dict['courses'] = courses
            context_dict['feedback'] = fb_with_colour
            context_dict['feedbackData'] = json.dumps(fbCat)
            context_dict['achievements'] = achievs
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

        fb_with_colour = {}
        for feedback in fb:
            try:
                stud_cat = Category.objects.get(name=feedback.category.name,user=request.user)
                fb_with_colour[feedback] = stud_cat.colour
            except:
                fb_with_colour[feedback] = feedback.category.colour

        context_dict['feedback'] = fb_with_colour
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

        context_dict['stud'] = stud
        context_dict['courses'] = stud.get_courses_with_score()

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
            lecturers = course.lecturers.all()
            students = course.students.all()
            top_students = students.order_by('-score')
            context_dict['course'] = course
            context_dict['lecturers'] = lecturers

            context_dict['students'] = students
            context_dict['sorted_students'] = course.get_leaderboard()
            fb = stud.get_fb_for_course(course.subject)

            fb_with_colour = {}
            for feedback in fb:
                try:
                    stud_cat = Category.objects.get(name=feedback.category.name,user=request.user)
                    fb_with_colour[feedback] = stud_cat.colour
                except:
                    fb_with_colour[feedback] = feedback.category.colour

            context_dict['feedback'] = fb_with_colour
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
    context_dict = {}

    if not request.user.is_authenticated or not request.user.is_student:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

    try:
        from_stud = StudentProfile.objects.get(student=request.user)
        stud_user = User.objects.get(id_number=student_number)

        if student_number == request.user.id_number:
            context_dict['error'] = "auth"
            return render(request,'student_feedback_app/general/error_page.html', context_dict)

        stud = StudentProfile.objects.get(student=stud_user)

        fb = stud.feedback_set.all().filter(from_user=request.user).order_by('-datetime_given')
        context_dict['from_student'] = from_stud
        context_dict['student'] = stud
        context_dict['feedback'] = fb
        course = Course.objects.get(subject_slug=subject_slug)
        context_dict['course'] = course

        context_dict['categories'] = request.user.category_set.all()
        context_dict['new_mess_form'] = NewMessageForm()

        messages = request.user.message_set.all()
        all_messages = {}
        for message in messages:
            all_messages[message.id] = message.text

        context_dict['messages'] = json.dumps(all_messages)

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

def lecturer_add_individual_feedback(request,subject_slug,student_number):
    context_dict = {}
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

    try:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        stud_user = User.objects.get(id_number=student_number)
        stud = StudentProfile.objects.get(student=stud_user)

        fb = stud.feedback_set.all().order_by('-datetime_given')
        context_dict['lecturer'] = lect
        context_dict['student'] = stud
        context_dict['feedback'] = fb
        course = Course.objects.get(subject_slug=subject_slug)
        context_dict['course'] = course

        context_dict['new_mess_form'] = NewMessageForm()

        context_dict['categories'] = request.user.category_set.all()

        messages = request.user.message_set.all()
        all_messages = {}
        for message in messages:
            all_messages[message.id] = message.text

        context_dict['messages'] = json.dumps(all_messages)
        context_dict['messages_qs'] = messages

        form = FeedbackForm()
        context_dict['form'] = form
        return render(request,'student_feedback_app/lecturer/lecturer_add_individual_feedback.html',context_dict)
    except:
        context_dict['student'] = None
        context_dict['feedback'] = None
        context_dict['error'] = "no_student"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)

def add_group_feedback(request,subject_slug):
    context_dict = {}
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
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

        context_dict['categories'] = request.user.category_set.all()

        context_dict['new_mess_form'] = NewMessageForm()

        messages = request.user.message_set.all()
        all_messages = {}
        for message in messages:
            all_messages[message.id] = message.text

        context_dict['messages'] = json.dumps(all_messages)
        context_dict['messages_qs'] = messages

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

        edit_cat_form = EditCategoryForm()
        context_dict["edit_cat_form"] = edit_cat_form

        new_cat_form = NewCategoryForm()
        context_dict["new_cat_form"] = new_cat_form

        new_mess_form = NewMessageForm()
        context_dict["new_mess_form"] = new_mess_form

        edit_mess_form = EditMessageForm()
        context_dict["edit_mess_form"] = edit_mess_form

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

    def post(self, request,format=None):
        cat = Category.objects.get(id=request.data.get('cat_id'),user=request.user)
        mess = Message.objects.get(id=request.data.get('mess_id'),user=request.user)
        if(request.data.get('type') == "GROUP"):
            # If providing group feedback then create a feedback object for every student
            # students = request.data.get('students')
            req_dict = dict(request.data)
            students = req_dict['students']
            for stud in students:
                stud_user = User.objects.get(id_number=stud)
                stud = StudentProfile.objects.get(student=stud_user)
                course = Course.objects.get(subject_slug=request.data.get('subject_slug'))

                fb = Feedback(pre_defined_message=mess,
                                category=cat,
                                optional_message = request.data.get('optional_message'),
                                student = stud,
                                points = request.data.get('points'),
                                from_user=request.user,
                                which_course = course)

                stud.score += int(request.data.get('points'))
                fb.save()
                cat.save()
                mess.save()
                stud_user.save()
                stud.save()
                course.save()
            return Response(status=status.HTTP_200_OK)
        else:
            # Otherwise just make one feedback for the individual student
            stud_user = User.objects.get(id_number=request.data.get('student'))
            stud = StudentProfile.objects.get(student=stud_user)
            course = Course.objects.get(subject_slug=request.data.get('subject_slug'))

            fb = Feedback(pre_defined_message=mess,
                            category=cat,
                            optional_message = request.data.get('optional_message'),
                            student = stud,
                            points = request.data.get('points'),
                            from_user=request.user,
                            which_course = course)

            stud.score += int(request.data.get('points'))
            fb.save()
            cat.save()
            mess.save()
            stud_user.save()
            stud.save()
            course.save()
            return Response(status=status.HTTP_200_OK)

class CategoryDetail(APIView):
    """
    Retrieve, create, update or delete a Category instance.
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

    def post(self, request,format=None):
        cat = Category(name=request.data.get('name'),
                        colour=request.data.get('colour'),
                        user=request.user)
        cat.save()
        return Response(status=status.HTTP_200_OK)

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

class MessageDetail(APIView):
    """
    Retrieve, create, update or delete a Message instance.
    """
    def get_object(self, mess_id):
        try:
            return Message.objects.get(id=mess_id)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, mess_id, format=None):
        message = self.get_object(mess_id)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def post(self, request,format=None):
        try:
            cat = Category.objects.get(id=request.data.get('category'))
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mess = Message(text=request.data.get('text'),
                        category=cat,
                        user=request.user)
        mess.save()
        cat.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, mess_id, format=None):
        message = self.get_object(mess_id)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, mess_id, format=None):
        message = self.get_object(mess_id)
        message.text = request.data.get('text')
        message.save()
        return Response(status=status.HTTP_200_OK)

class StudentCourseRelDestroy(APIView):
    def delete(self, request, student_id, course_code, format=None):
        course = Course.objects.get(course_code=course_code)
        user = User.objects.get(id_number=student_id)
        student = StudentProfile.objects.get(student=user)
        course.students.remove(student)
        student.courses.remove(course)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedbackSortedByPoints(generics.ListAPIView):
    queryset = Feedback_full.objects.all().order_by('-points')
    serializer_class = Feedback_fullSerializer

class FeedbackSortedByDate(generics.ListAPIView):
    queryset = Feedback_full.objects.all().order_by('-datetime_given')
    serializer_class = Feedback_fullSerializer

class FeedbackSortedByCourse(generics.ListAPIView):
    queryset = Feedback_full.objects.all().order_by('courseName')
    serializer_class = Feedback_fullSerializer

class Feedback_full(generics.ListAPIView):
    queryset = Feedback_full.objects.all()
    serializer_class = Feedback_fullSerializer

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            populate_categories_and_messages(user)
            login(request, user)
            if user.is_lecturer:
                return redirect('lecturer_home')
            else:
                return redirect('student_home')
    else:
        form = RegisterForm()
    return render(request, 'registration/registration_form.html', {'form': form})


def invites(request):
    context_dict = {}
    if not request.user.is_authenticated or not request.user.is_lecturer:
        context_dict['error'] = "auth"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)
    try:
        if request.method == 'GET':
            token = request.GET.get('token', '')
            context_dict['token'] = token
            if token == '' or Course.objects.filter(course_token=token).count() == 0:
                return redirect('lecturer_courses')
            course = Course.objects.get(course_token=token)
    except:
        context_dict['error'] = "error"
        return render(request,'student_feedback_app/general/error_page.html', context_dict)


    mode = 0
    message =  ' lecturer ' + request.user.username + ' has invited you to join ' + course.subject + ' (' + course.course_code + '). To join this course use this token: ' + course.course_token
    students_string = request.COOKIES.get("students")
    if is_json(students_string):
        mode += 1
        students_list = json.loads(students_string)
        students = []
        for student_id in students_list:
            stud_user = User.objects.get(id_number=student_id)
            students.append(stud_user)

        for student in students:
            personal_message = 'Dear ' + student.username + message
            send_mail('You are invited to join a course!',personal_message,'lect.acc.unicom@gmail.com',[student.email])
    message =  ' Lecturer ' + request.user.username + ' has invited you to join ' + course.subject + ' (' + course.course_code + '). To join this course use this token: ' + course.course_token
    students_emails_string = request.COOKIES.get("emails")
    if is_json(students_emails_string):
        mode += 1
        emails_list = json.loads(students_emails_string)
        emails = []
        for email in emails_list:
            if email != "example@university.com":
                emails.append(email)
        message = message + "; Register online to joint UniCom."
        send_mail('You are invited to join a course!',message,'lect.acc.unicom@gmail.com',emails)
    if mode == 0:
        lect = LecturerProfile.objects.get(lecturer=request.user)
        students = lect.get_my_students()
        added_students = course.students.distinct()
        context_dict['students'] = set(students).difference(set(added_students))
        return render(request, 'student_feedback_app/lecturer/invites.html', context_dict)
    response = lecturer_course(request, course.subject_slug)
    response.set_cookie('students', '', path="/lecturer/invites/")
    response.set_cookie('emails', '', path="/lecturer/invites/")
    return response

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def populate_categories_and_messages(user):
    # This uses newly created methods in the population script to ensure that
    # every user gets the list of categories and messages upon registration
    add_categories_for_user(user)
    add_messages_for_user(user)
