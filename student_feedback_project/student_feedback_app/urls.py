from django.conf.urls import re_path, include
from student_feedback_app import views
from student_feedback_app.models import Category
from student_feedback_app.forms import FeedbackForm
from dal import autocomplete
from django.views import generic
from student_feedback_app.views import CategoryAutocomplete

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^student/home/$', views.student_home, name='student_home'),
    re_path(r'^student/all-feedback/$', views.all_feedback, name='all_feedback'),
    re_path(r'^student/my-courses/$', views.my_courses, name='my_courses'),
    re_path(r'^lecturer/home/$', views.lecturer_home, name='lecturer_home'),
    re_path(r'^lecturer/my-provided-feedback/$', views.my_provided_feedback, name='my_provided_feedback'),
    re_path(r'^lecturer/create-course/$', views.create_course, name='create_course'),
    re_path(r'^lecturer/courses/$', views.lecturer_all_courses, name='lecturer_all_courses'),
    re_path(r'^lecturer/courses/(?P<subject_slug>[\w\-]+)/$', views.lecturer_course, name='lecturer_course'),
    re_path(r'^lecturer/(?P<subject_slug>[\w\-]+)/(?P<student_number>[\w\-]+)/add-feedback/$', views.add_feedback, name='add_feedback'),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    re_path(r'^lecturer/(?P<student_number>[\w\-]+)/$', views.lecturer_view_student, name='lecturer_view_student'),
    re_path(r'^category-autocomplete/$', CategoryAutocomplete.as_view(model=Category,create_field='name'), name='category_autocomplete'),
    re_path(r'^create-category/(?P<name>[\w\-]+)/$', generic.UpdateView.as_view(model=Category,form_class=FeedbackForm)),
]
