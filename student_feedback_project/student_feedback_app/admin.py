from django.contrib import admin
from student_feedback_app.models import User, Category, Message, Feedback, LecturerProfile, StudentProfile, Course
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Feedback)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
admin.site.register(Course)
