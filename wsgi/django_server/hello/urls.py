from django.urls import path

from . import views

urlpatterns = [
    path(r'say/', views.say, name='say')
]