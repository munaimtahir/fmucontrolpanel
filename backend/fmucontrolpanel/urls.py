"""
URL configuration for fmucontrolpanel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/update-status/', views.update_project_status, name='update_project_status'),
    path('task/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task_status'),
    path('today/', views.today_view, name='today'),
    path('review-merge/', views.review_merge_queue, name='review_merge'),
    path('webhooks/github/', views.github_webhook, name='github_webhook'),
    path('admin/', admin.site.urls),
]
