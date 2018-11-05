import time
import threading

from django.http import JsonResponse

from app_model.models import Article
from .tasks import create_random_user_accounts


def perform_celery_task(request):
    # ret = create_random_user_accounts.delay(100)
    # if request.GET.get('test'):
    #     import pdb; pdb.set_trace()
    #     time.sleep(5)

    print('----> {}'.format(threading.get_ident()))
    
    if request.GET.get('test'):
        for i in range(10000000):
            for j in range(100000000):
                pass
        
    return JsonResponse({
        'result':'success',
        # 'id': id(Article.objects.first()),
        'id': threading.get_ident(),
    })