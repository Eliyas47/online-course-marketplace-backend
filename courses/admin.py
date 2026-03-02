from django.contrib import admin
from .models import Category, Course, Section, Lesson, Module, LessonProgress


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(Module)
admin.site.register(LessonProgress)

