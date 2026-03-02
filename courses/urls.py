from django.urls import path
from .views import CourseListView, CourseDetailView, CourseCreateView, InstructorDashboardView, LessonDetailView
from .views import CourseLearnView
from .views import CreateModuleView, CreateLessonView


urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("create/", CourseCreateView.as_view(), name="course-create"),
    path("<int:pk>/learn/", CourseLearnView.as_view(), name="course-learn"),
    path("modules/create/", CreateModuleView.as_view()),
    path("lessons/create/", CreateLessonView.as_view()),
    path("lessons/<int:pk>/", LessonDetailView.as_view()),
    path("dashboard/", InstructorDashboardView.as_view()),
]