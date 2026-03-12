from django.urls import path
from .views import (
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView,
    InstructorDashboardView, LessonDetailView, CourseLearnView,
    CreateModuleView, CreateLessonView
)


urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("<uuid:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("<uuid:pk>/update/", CourseUpdateView.as_view(), name="course-update"),
    path("<uuid:pk>/learn/", CourseLearnView.as_view(), name="course-learn"),
    path("create/", CourseCreateView.as_view(), name="course-create"),
    path("modules/create/", CreateModuleView.as_view(), name="module-create"),
    path("lessons/create/", CreateLessonView.as_view(), name="lesson-create"),
    path("lessons/<uuid:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
    path("dashboard/", InstructorDashboardView.as_view(), name="instructor-dashboard"),
]