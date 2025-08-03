
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('programs/', views.programs_view, name='programs_view'),
    path('program/<int:pk>/', views.program_detail, name='program_detail'),
    path('modules/', views.modules_view, name='modules_view'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
]
