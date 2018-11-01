from django.http import JsonResponse

from app_model.models import Article
from .tasks import create_random_user_accounts


def perform_celery_task(request):
    ret = create_random_user_accounts.delay(100)
    
    return JsonResponse({
        'result':'success',
        'id': id(Article.objects.first()),
    })