from django.http import JsonResponse
from django.urls import reverse


def get_url(request):
    return JsonResponse({
        'result':'success',
        'url': reverse('my-app:get-url'),   
    })