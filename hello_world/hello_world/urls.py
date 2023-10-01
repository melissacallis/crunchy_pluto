"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views



urlpatterns = [
    path("", views.index),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('user_form/', views.user_form, name='user_form'),
    path('user_form/<str:username>/', views.user_form, name='edit_user_form'),
    path('user_profile/<str:username>/', views.view_user_profile, name='view_user_profile'),
    path('success_demo/<str:username>/', views.success_demo, name='success_demo'),
    path('user_form/<str:username>/success_skills/', views.success_skills, name='success_skills'),
    path('user_form/<str:username>/edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('user_form/<str:username>/success_skills/', views.edit_skills, name='edit_skills'),
    path('add_skills/<str:username>/', views.add_skills, name='add_skills'),
    path('user_form/<str:username>/success_skills/', views.success_skills, name='success_skills'),
    path('edit_skills/<str:username>/', views.edit_skills, name='edit_skills'),
    path('edit_skills/<str:username>/<int:skill_id>/', views.edit_skills, name='edit_skills'),
    path('delete_skill/<str:username>/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('add_experience/<str:username>/', views.add_experience, name='add_experience'),
    path('add_experience/<str:username>/<int:experience_id>/', views.add_experience, name='add_experience'),
    path('edit_experience/<str:username>/<int:experience_id>/', views.edit_experience, name='edit_experience'),
    path('edit_experience/<str:username>/', views.edit_experience, name='edit_experience'),
    path('delete_experience/<str:username>/<int:experience_id>/', views.delete_experience, name='delete_experience'),
    path('add_education/<str:username>/', views.add_education, name='add_education'), 
    path('edit_education/<str:username>/<int:education_id>/', views.edit_education, name='edit_education'),
    path('delete_education/<str:username>/<int:education_id>/', views.delete_education, name='delete_education'),


   




]


