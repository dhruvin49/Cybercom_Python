from django.contrib import admin
from .models import *



class ExperienceInline(admin.TabularInline):
    model = Experience

class EducationInline(admin.TabularInline):
    model = Education

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'password')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    inlines = [ExperienceInline, EducationInline]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Holiday)


