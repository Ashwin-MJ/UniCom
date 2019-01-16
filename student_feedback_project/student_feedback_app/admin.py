from django.contrib import admin
from student_feedback_app.models import User, Category, Message, Feedback, LecturerProfile, StudentProfile, Course
# Register your models here.
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Feedback)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
admin.site.register(Course)

def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = "Mark selected users as active"

class PendingApproval(User):
    class Meta:
        proxy = True

class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(is_lecturer = True, is_active = False)
    list_display = ['is_active', 'date_joined', 'id_number', 'username']
    ordering = ['date_joined']
    actions = [make_active]
    
admin.site.register(PendingApproval, UserAdmin)
admin.site.register(User)
