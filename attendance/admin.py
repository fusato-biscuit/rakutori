from django.contrib import admin
from .models import Uezu_seminar
# Register your models here.

class Uezu_seminarAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'attended_day')


admin.site.register(Uezu_seminar, Uezu_seminarAdmin)
