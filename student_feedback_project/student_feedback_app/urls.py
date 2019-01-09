from django.conf.urls import re_path, include
from student_feedback_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^student/home/$', views.student_home, name='student_home'),
    re_path(r'^student/all-feedback/$', views.all_feedback, name='all_feedback'),
    re_path(r'^student/my-classes/$', views.my_classes, name='my_classes'),
    re_path(r'^lecturer/home/$', views.lecturer_home, name='lecturer_home'),
    re_path(r'^lecturer/my-provided-feedback/$', views.my_provided_feedback, name='my_provided_feedback'),
    re_path(r'^lecturer/create-class/$', views.create_class, name='create_class'),
    re_path(r'^lecturer/classes/$', views.lecturer_all_classes, name='lecturer_all_classes'),
    re_path(r'^lecturer/classes/(?P<subject_slug>[\w\-]+)/$', views.lecturer_class, name='lecturer_class'),
    re_path(r'^lecturer/(?P<subject_slug>[\w\-]+)/(?P<student_number>[\w\-]+)/add-feedback/$', views.add_feedback, name='add_feedback'),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    re_path(r'^lecturer/(?P<student_number>[\w\-]+)/$', views.lecturer_view_student, name='lecturer_view_student'),
    re_path(r'^FeedbackSortedByPoints/$', views.FeedbackSortedByPoints.as_view()),
    re_path(r'^FeedbackSortedByDate/$', views.FeedbackSortedByDate.as_view()),
    re_path(r'^FeedbackSortedByClass/$', views.FeedbackSortedByClass.as_view()),
    re_path(r'^CategoryList/$', views.CategoryList.as_view()),
    re_path(r'^Feedback_with_categoryList/$', views.Feedback_with_categoryList.as_view()),
    re_path(r'^Feedback_with_studentList/$', views.Feedback_with_studentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
