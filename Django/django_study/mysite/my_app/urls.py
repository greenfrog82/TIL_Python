from django.urls import path

from . import views

urlpatterns = [
    path(r'get-url/', views.get_url, name='get-url'),
]