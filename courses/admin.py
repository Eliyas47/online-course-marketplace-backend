from django.contrib import admin
from .models import Category, Course, Module, Lesson, LessonProgress


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(LessonProgress)