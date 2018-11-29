from django.urls import path, re_path

from . import views

urlpatterns = [
    # path(r'get-url/', views.get_url, name='get-url'),
    re_path(r'get-url/', 'my_app.views.get_url', name='get-url'),
]