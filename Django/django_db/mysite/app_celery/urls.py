from django.urls import path

from . import views

urlpatterns = [
    path(r'perform-task/', views.perform_celery_task, name='perform_celery_task'),
]