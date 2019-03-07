from django.conf.urls import re_path, include
from student_feedback_app import views
from rest_framework.urlpatterns import format_suffix_patterns
from student_feedback_app.models import Category, Message


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^category/$', views.CategoryDetail.as_view(), name="category"),
    re_path(r'^message/$', views.MessageDetail.as_view(), name="message"),
    re_path(r'^feedback/$', views.FeedbackDetail.as_view(), name="feedback"),
    re_path(r'^message/(?P<mess_id>[\w\-]+)/$', views.MessageDetail.as_view(), name="message_detail"),
    re_path(r'^category/(?P<cat_id>[\w\-]+)/$', views.CategoryDetail.as_view(), name="category_detail"),
    re_path(r'^feedback/(?P<fb_id>[\w\-]+)/$', views.FeedbackDetail.as_view(), name="feedback_detail"),
    re_path(r'^my-profile/$', views.my_profile, name='my_profile'),
    re_path(r'^customise-options/$', views.customise_options, name='customise_options'),
    re_path(r'^view-profile/(?P<student_number>[\w\-]+)/$', views.view_profile, name='view_profile'),
    re_path(r'^student/home/$', views.student_home, name='student_home'),
    re_path(r'^student/all-feedback/$', views.student_all_feedback, name='student_all_feedback'),
    re_path(r'^student/my-provided-feedback/$', views.my_provided_feedback, name='student_provided_feedback'),
    re_path(r'^student/courses/(?P<subject_slug>[\w\-]+)/$', views.student_course, name='student_course'),
    re_path(r'^student/courses/$', views.student_courses, name='student_courses'),
    re_path(r'^student/(?P<subject_slug>[\w\-]+)/(?P<student_number>[\w\-]+)/add-individual-feedback/$', views.student_add_individual_feedback,
            name='student_add_individual_feedback'),
    re_path(r'^lecturer/home/$', views.lecturer_home, name='lecturer_home'),
    re_path(r'^lecturer/courses/$', views.lecturer_courses, name='lecturer_courses'),
    re_path(r'^lecturer/invites/$', views.invites, name='invites'),
    re_path(r'^lecturer/my-provided-feedback/$', views.my_provided_feedback, name='lecturer_provided_feedback'),
    re_path(r'^lecturer/courses/(?P<subject_slug>[\w\-]+)/$', views.lecturer_course, name='lecturer_course'),
    re_path(r'^lecturer/courses/(?P<subject_slug>[\w\-]+)/add-group-feedback/$', views.add_group_feedback,
            name='add_group_feedback'),
    re_path(r'^lecturer/(?P<subject_slug>[\w\-]+)/(?P<student_number>[\w\-]+)/add-individual-feedback/$', views.lecturer_add_individual_feedback,
            name='lect_add_individual_feedback'),
    re_path(r'^accounts/register/$', views.register, name='register'),
    re_path(r'^unapproved/$', views.unapproved, name="unapproved"),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    re_path(r'^FeedbackSortedByPoints/$', views.FeedbackSortedByPoints.as_view()),
    re_path(r'^FeedbackSortedByDate/$', views.FeedbackSortedByDate.as_view()),
    re_path(r'^FeedbackSortedByCourse/$', views.FeedbackSortedByCourse.as_view()),
    re_path(r'^Fedback_full/$', views.Feedback_full.as_view()),
    re_path(r'^StudentCourseRelDestroy/(?P<student_id>[\w\-]+)/(?P<course_code>[\w\-]+)/$', views.StudentCourseRelDestroy.as_view(), name='student_rel_destroy'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
