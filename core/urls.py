
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('programs/', views.programs_view, name='programs_view'),
    path('program/<int:pk>/', views.program_detail, name='program_detail'),
    path('modules/', views.modules_view, name='modules_view'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
    path('lecturers/', views.lecturers_view, name='lecturers_view'),
    path('lecturer/<int:pk>/', views.lecturer_detail, name='lecturer_detail'),
    path('resources/', views.resources_view, name='resources_view'),
    path('login/', views.student_login, name='student_login'),
    path('signup/', views.student_signup, name='student_signup'),
    path('logout/', views.student_logout, name='student_logout'),
]
