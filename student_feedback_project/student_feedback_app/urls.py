from django.conf.urls import re_path, include
from student_feedback_app import views
from rest_framework.urlpatterns import format_suffix_patterns
from student_feedback_app.models import Category, Message
from student_feedback_app.views import CategoryAutocomplete, MessageAutocomplete


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^category/(?P<cat_id>[\w\-]+)/$', views.CategoryDetail.as_view(), name="category_detail"),
    re_path(r'^feedback/(?P<fb_id>[\w\-]+)/$', views.FeedbackDetail.as_view(), name="feedback_detail"),
    re_path(r'^my-profile/$', views.my_profile, name='my_profile'),
    re_path(r'^edit-bio/$', views.edit_bio, name='edit_bio'),
    re_path(r'^student/home/$', views.student_home, name='student_home'),
    re_path(r'^student/all-feedback/$', views.student_all_feedback, name='student_all_feedback'),
    re_path(r'^student/my-provided-feedback/$', views.my_provided_feedback, name='student_provided_feedback'),
    re_path(r'^student/courses/(?P<subject_slug>[\w\-]+)/$', views.student_course, name='student_course'),
    re_path(r'^student/courses/$', views.student_courses, name='student_courses'),
    re_path(r'^student/(?P<subject_slug>[\w\-]+)/(?P<student_number>[\w\-]+)/add-individual-feedback/$', views.student_add_individual_feedback,
            name='student_add_individual_feedback'),
    re_path(r'^lecturer/home/$', views.lecturer_home, name='lecturer_home'),
    re_path(r'^lecturer/create-course/$', views.create_course, name='create_course'),
    re_path(r'^lecturer/courses/$', views.lecturer_courses, name='lecturer_courses'),
    re_path(r'^lecturer/my-provided-feedback/$', views.my_provided_feedback, name='lecturer_provided_feedback'),
    re_path(r'^lecturer/customise-options/$', views.lecturer_customise_options, name='lecturer_customise_options'),
    re_path(r'^lecturer/courses/(?P<subject_slug>[\w\-]+)/$', views.lecturer_course, name='lecturer_course'),
    re_path(r'^lecturer/courses/(?P<subject_slug>[\w\-]+)/add-group-feedback/$', views.add_group_feedback,
            name='add_group_feedback'),
    re_path(r'^lecturer/(?P<subject_slug>[\w\-]+)/(?P<student_number>[\w\-]+)/add-individual-feedback/$', views.lecturer_add_individual_feedback,
            name='lect_add_individual_feedback'),
    re_path(r'^accounts/register/$', views.register, name='register'),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    re_path(r'^FeedbackSortedByPoints/$', views.FeedbackSortedByPoints.as_view()),
    re_path(r'^FeedbackSortedByDate/$', views.FeedbackSortedByDate.as_view()),
    re_path(r'^FeedbackSortedByCourse/$', views.FeedbackSortedByCourse.as_view()),
    re_path(r'^CategoryList/$', views.CategoryList.as_view()),
    re_path(r'^Feedback_with_categoryList/$', views.Feedback_with_categoryList.as_view()),
    re_path(r'^Feedback_with_studentList/$', views.Feedback_with_studentList.as_view()),
    re_path(r'^Feedback_with_from_userList/$', views.Feedback_with_from_userList.as_view()),
    re_path(r'^lecturer/view-student/(?P<student_number>[\w\-]+)/$', views.lecturer_view_student, name='lecturer_view_student'),
    re_path(r'^category-autocomplete/$', CategoryAutocomplete.as_view(model=Category,create_field='name'), name='category_autocomplete'),
    re_path(r'^message-autocomplete/$', MessageAutocomplete.as_view(model=Message,create_field='text'), name='message_autocomplete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
