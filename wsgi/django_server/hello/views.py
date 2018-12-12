from django.http import JsonResponse

def say(request):
    return JsonResponse({'res': 'Hello'})