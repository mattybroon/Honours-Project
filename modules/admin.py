from django.contrib import admin
from .models import Module, Student, StudentMark

admin.site.register(Module)
admin.site.register(Student)
admin.site.register(StudentMark)