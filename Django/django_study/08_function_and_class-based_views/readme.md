# 8. Function- and Class-Based Views

Django에는 Function-Based Views(FBVs)와 Class-Based Views(CBVs)가 있다. 여기서 이 둘에 대해서 이해해보도록 하자.  

## 8.1 When to Use FBVs or CBVs

view를 개발할 때, FBV 또는 CBV중 어떤 것을 선택해야하는지 늘 생각해야한다. 어떤 view는 CBV가 좋은 선택일 수 있고, 어떤 view는 FBV가 좋은 선택일 수 있다.   

책에서는 가급적 CBV를 사용하고, 만약 이를 통한 구현이 어려운 경우 FBV를 선택하라고 가이드하고 있다.  
그러면서도 대부분의 view를 FBV로 개발하고 서브클래싱이 필요한 경우에만 CBV를 선택해도 된다고 되어있다. 우리는 어떻게 쓰고 있고, 어떻게 쓰는게 더 좋다고 생각하는지?

이 부분에 대해서 스터디 참여인원과 이야기해본 결과 다음과 같은 의견이 나왔다. 

>1. 하나의 Resource에 대해서 CRUD가 있다면, CBV로 개발하고 그렇지 않고 특정 Resource에 대해서 CRUD 중 하나만 한다면 FBV로 개발하는것이 편리하겠다. 
2. FBV로 개발해보고 CBV로 접근하는 방법도 있다.

위 의견에서 첫번째 의견을 먼조 검토해보면, CBV냐 FBV냐에 대한 선택을 디자인측면에서 본것이 아니라 기능적인 측면에서 본것 같다. 예를들어 `View`클래스를 상속하면 CRUD에 해당하는 HTTP Method들을 클래스 메소드로 제공하는데 이를 통해 쉽게 특정 Resource에 대한 CRUD가 가능하기 때문에 이와같은 이야기가 나온것 같다. 마찬가지로 특정 Resource에 대해서 FBV개발하는 것이 편하다는 것 역시 같은 맥락이다. 
여기서 난 의견이 좀 다른것이 어떤 것을 구현해도 딱히 쉽거나 어렵지 않다고 보지만 `가독성`과 `재활용성`면에서 접근이 필요한데 `DjangoRestFramework`를 보면 `CBV`의 사용을 극대화 해서 기능을 은닉화 해서 `가독성`을 높이고 OOP 개념을 이용하므로서 각각 `CBV`에 구현된 기능을 `재활용`하기 쉽게 구현해두었다. 
어쩌면 이 책은 OOP 개념을 이용하라고 이야기하고 있는지 모른다. 그리고 `DjangoRestFramework`가 이러한 개념을 잘 활용한 예가 아닌가 싶다. 

두번째 의견 역시 앞서의 생각과 같이 `FBV`로 먼저 개발해본다는 것은 OOP에 대한 접근이 어렵거나 미숙해서 그런게 아닌가 싶다. 역시 앞서와 같은 결론이다. 책에서는 OOP 개념을 사용하라는것이고 나 역시 여기에 동의한다. 

## 8.2 Keep View Logic Out of URLConfs

클라이언트의 요청은 `URLConfs`를 통해 view로 라우팅 된다. 이러한 `URLConfs`를 `urls.py`모듈에 정의한다.   
Django의 URL 디자인 철학은 다음과 같다.  

>### [URL Design](https://docs.djangoproject.com/en/2.1/misc/design-philosophies/#url-design)
>#### Loose coupling
>Django app의 urls.py 모듈은 파이썬 코드와 결합되어서는 안된다. urls.py 모듈에 파이썬 함수 이름을 작성하는 것은 나쁘고 추악한 일이다.
>
>Django의 URL 시스템은 urls.py 모듈이 동일한 앱의 다른 상황에서 다른 행동을 수행할 수 있도록 해야한다. 예를들어, 하나의 사이트는 스토리를 /stories/라는 URL을 통해서 저장할 수 있도 있지만 /news/라는 URL을 통해서도 할 수 있을 것이다. 
>
>#### Infinite flexibility
>URL은 가능한 유연해야한다. 상상할 수 있는 어떤 URL 디자인이라도 가능해야한다. 
>
>#### Encourage best practices
>프레임워크는 개발자가 URL을 보기 좋고 쉽게 디자인할 수 있도록 한다.  
>웹 페이지에서 파일 확장자와 콤마등은 허용되지 않는 등 URL을 작성하는 기존 Best Practice를 권장한다. 
>
>####Definitive URLs
>기술적으로 foo.com/bar와 food.com/bar/는 서로 다른 URL이고 search-engine robots들 역시 이들은 서로 다른 페이지로 인식한다. 따라서 URL을 작성할 때 search-engine robots이 혼란스럽지 않도록 `normalize`에 신경써야한다.  
>
>이것이 `APPEND_SLASH` 설정을 넣어놓은 숨은 이유이다. 
>참고로 `APPEND_SLASH` 설정을 `True`로 하면 foo.com/bar가 URLConf에 존재하지 않으면 foo.com/bar/와 같이 주소의 마지막에 `/`를 붙여서 `리다이렉트`해준다.  

Django의 URL를 정의하는 두가지 원칙은 다음과 같다.   

1. views 모듈은 오직 view 로직만을 포함해야한다. 
2. url 모듈은 오직 url 로직만을 포함해야한다.  

다음과 같은 코드를 본적이 있는가? 아마도 Django의 공식 튜토리얼에 있는 코드이다.  

Example 8.1
```python
from django.conf.urls import url
from django.views.generic import DetailView

from tastings.models import Tasting

 urlpatterns = [ 
     url(r'ˆ(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Tasting,
            template_name='tastings/detail.html'),
        name='detail'),
    url(r'^?P<pk>\d+)/results/$', 
        DetailView.as_view(
            model=Tasting,
            template_name='tastings/results.html'),
        name='results'),
]
```


위 예제가 정말 잘못된 것인가? 우리도 이렇게 쓰는 경우가 있는데 ..
내 생각에 공통 코드에 파라미터를 달리해서 처리할 수 있는 view가 있다고 하면 이렇게 쓰는것도 괜찮아 보이는데?
책에 나오는 단점들도 잘 이해가 되지 않는다. 오히려 함수에 파라미터를 넘겨서 다양한 결과를 받아내는 것과 같이 일반화된 view를 잘 재활용하고 있다고 생각하기 때문이다.  

이 부분에 대해서 스터디 참여인원들과 토의해본 결과는 책에서와 같이 둘을 분리해놓는것이 좋다는쪽으로 의견이 모아졌다. 이에 대한 근거로 개발자들은 url을 보고 view를 찾아 동작을 살피는데 이에 대한 예외를 두는것이 좋아보이지 않고 예외를 두는것에 대해 특별한 장점이 보이지 않는다는 것이다. 

위와 같이 논의가 되었지만 아직도 납득이 되지 않는다. 하지만 Django와 이 책 그리고 스터디 참여인원들의 생각이 하나이므로 따르는것이 좋겠다.  

## 8.3 Stick to Losse Coupling in URLConfs

여기서는 앞서 언급했던 URLconf와 view가 타이트하게 결합되는 문제를 회피하는 방법에 대해서 알아보자.   

먼저, view를 작성하자. 

```python
# tastings/views.py
from django.views.generic import ListView, DetailView, UpdateView
from djngo.core.urlresolvers import reverse

from .models import Tasting

class TasteListView(ListView):
    model = Tasting

class TasteDetailView(DetailView):
    model = Tasting

class TasteResultView(TesteDetailView):
    template_name = 'tastings/results.html'

class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse('tastings:detail', kwargs={'pk': self.object.pk})o
```

앞서 작성했던, URLConf를 개선해보자. 

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.TasteListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>\d+)$',
        view=views.TasteDetailView.as_view(),
        name='results'
    ),
    url(
        regex=r'^(?P<pk>\d+)/results/$',
        view=views.TasteDetailView.as_view(),
        name='results'
    ),
    url(
        regex=r'^(?P<pk>\d+)/update/$',
        view=views.TasteUpdateView.as_view(),
        name='update'
    )
]
```

얼핏보면, 앞선 예제보다 코드가 늘어났기 때문에 오히려 비합리적으로 보이지만 다음 원칙들을 모두 만족시키고 있다.   

* **Don't Repeat Yourself**: views들이 인자 또는 속성을 반복하지 않는다. 
* **Loose coupling**: URLConf로부터 `model`의 이름과 `template`이름을 분리하였다. view는 수정없이 하나 또는 여러 URLConf에서 호출 가능해야한다. 
* **URLConfs should do one thing and do it well**: 앞서 이야기한바와 같이, URLConfs는 오직 URL을 라우팅하는 역할만 수행해야한다. 이를 통해 URLConf로 전달되는 view 로직을 확인한 후 다시 view의 코드를 확인할 필요가 없이 오직 view코드만을 확인하면 된다.   
* **Our views benefit from being class-based**: 구조가 잘 만들어진 CBV를 다른 클래스에서 상속할 수 있다. 이를 통해 Authentication, Authorization, New contents format 또는 여러 비즈니스 요구를 쉽게 핸들링 할 수 있다.
* **Infinite flexibility**: view가 일관되게 정의되어 있기 때문에, 각각의 비즈니스 로직을 구현할 수 있다. 

위 부분은 책에 소개된 내용인데 `Our views benefit from being class-based`과 `Infinite flexibility` 부분은 URLConf에서 로직을 분리하면서 나타나는 효과가 아닌것 같고 `CBV`를 활용했을 때의 장점이 아닌가 싶다. 

### 8.3.1 What if We Aren't Using CBVs?

앞서는 `CBV`를 통해 `view`와 `URLConfs`를 분리하는 방법에 대해서 설명했지만, `FBV`를 사용하는 경우 역시 동일한 원칙을 가져가면 된다.  

>Keep logic out of URLConfs!

## 8.4 Use URL Namespaces

`URL Namespace`은 어플리케이션 레벨과 인스턴스 레벨의 네임스페이스를 구분하기위해 사용된다. `URL Namespace`는 별 도움이 될것같지 않지만, 일단 사용해본 개발자들은 왜 미리 이 기능을 사용하지 않았을까하고 되물을 정도로 유용하다. `URL Namesapce`의 용법을 요약하면 다음과 같다.  

>tastings_detail과 같은 URL 이름을 사용하지 말고, tastings:detail을 사용해라.   

`Django 2.1`에서는 책에서와 같이 `include`함수에 `namespace`keyword argument를 전달해보자. 

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-app/', include('my_app.urls', namespace='my-app')), 
]
```

다음과 같은 에러가 발생한다.   

```bash
  File "/Users/a201808045/github/TIL_Python/Django/django_study/mysite/mysite/urls.py", line 21, in <module>
    path('myapp/', include('my_app.urls', namespace='old')),
  File "/Users/a201808045/.virtualenv/django/lib/python3.7/site-packages/django/urls/conf.py", line 39, in include
    'Specifying a namespace in include() without providing an app_name '
django.core.exceptions.ImproperlyConfigured: Specifying a namespace in include() without providing an app_name is not supported. Set the app_name attribute in the included module, or pass a 2-tuple containing the list of patterns and app_name instead.
```

원인은 `Django 2.1`에서 `include`함수의 signiture가 변경되어 그렇다. 다음은 `Django 2.1`에서의 `include`함수의 signiture이다.  

[include](https://docs.djangoproject.com/en/2.1/ref/urls/#include)
```python
include(module, namespace=None)
include(pattern_list)
include((pattern_list, app_namespace), namespace=None)
```

`Django 2.1`의 `include`함수의 signiture로 옳바르게 수정하면, 다음과 같다. 

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-app/', include(('my_app.urls', 'my-app'), namespace='my-app')),
]
```

`URL Namespace`의 사용방법을 익혔으니, 이제 이것이 왜 유용한지 알아보자. 

### 8.4.1 Makes for Shorter, More Obvious and Don't Repeat Yourself URL Names

앞서 책의 예제에서는 'tastings_detail'과 'tastings_results'와 같이 모델 또는 앱 이름을 prefix로 사용하는 URL이름을 사용하지 않았다. 대신에 'detail'과 'results'와 같이 간단명료한 이름을 사용하였다. 이것은 가독성을 매우 좋게한다. 특히 Django 초보자들에게 더 그렇다. (아마도 tastings_라는 prefix를 붙이는 이유를 고민해야할테니까 ..)

또한, 누가 'tastings'던 무엇이 되었던간에 URL의 이름을 작성할 때 이러한 prefix를 매번 코딩하길 원하는 개발자가 누가있겠는가? 

### 8.4.2 Increases Interporability With Third-Party Libraries

\<myapp\>_detail과 같은 URL이름을 사용하는 경우 발생하는 문제 중 하나는 앱 이름이 충돌되는 경우이다. 물론 자신이 작성하는 앱의 이름이 충돌되는 경우는 없을것이다. 하지만 Third-Party 앱을 사용하는데, 공교롭게도 이름이 갖다고 가정하자. 이런 경우, `URL Namesapce`를 사용하면 문제를 쉽게 해결할 수 있다.  

**CHECK**

앱 이름이 겹치는 경우에 대한 예제를 작성하지 못하겠다. 어떻게 작성하지?

### 8.4.4. Allow for More App and Template Reverse Tricks

`URL Namespace`을 사용하는 몇몇 트릭들이 존재하지만, 대부분의 경우 이것을 사용해야하는 정당한 이유가 없기 때문에 이 책에서는 이를 소개하지 않는다. 사실, 이러한 트릭을 사용하는것은 실질적인 이득은 없고 프로젝트를 더 복잡하게 만든다. 그러나 다음 두가지 경우에 있어서는 유용하다. 

1. django-debug-toolbar와 같이 개발툴에서 디버깅 목적으로 서비스를 모니터링하고자 하는 경우.
2. 사용자가 'modules'을 추가하고 바꿔서 사용자별 동작을 달리하고자 할 경우. (마치 플러그인 처럼?)

개발자들은 이러한 창의적인 `URL Namesapce` 트릭의 사용을 정당화하지만, 늘 그렇듯이 가장 단순한 방법부터 시도해보아라. 

**CHECK**

혹시 1, 2이 어떻게 동작하는지 알고있는 분?

## 8.5 Don't Reference Views as Strings in URLConfs

Django 1.8의 튜토리얼이 배포되기 전 버전의 튜토리얼들에서 종종 urls.py 모듈에 view를 맵핑할 때 문자열을 사용하는 경우가 종종 보인다. 

>참고로, 아래 예제는 책에 나오는 예제로 Django 1.10버전에서부터 `patterns`라는 함수가 사라졌다.

```python
urlpatterns = patterns('', 
    url(r'^$', 'polls.views.index', name='index'),
)
```

위와같이 view를 맵핑할 때 문자열을 사용하는 방법은 다음 두가지 문제를 가지고 있다. 

1. Django는 마법과같이 view를 추가한다. 이러한 경우 view에 에러가 있다면 디버깅하기가 어렵다.
2. Django의 숙련자는 Django 초보자에게 `urlpatterns`변수가 왜 필요한지 설명해야한다.  

**CHECK**

위 내용이 공감이 가는가? 실제 우리 코드도 위와같이 많이 쓰고 있음.  

따라서, 다음과 같이 작성하는것이 옳은 방법이다.  

```python
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

위 anti-pattern을 `Django 2.1`에서 재현해보자. 

```python
from django.urls import path

from . import views

urlpatterns = [
    # path(r'get-url/', views.get_url, name='get-url'),
    path(r'get-url/', 'my_app.views.get_url', name='get-url'),
]
```

Django의 runserver command를 실행해보면 다음과 같은 에러가 발생한다.   
따라서, `Django 2.1`을 사용하는 경우 위와 같은 문제를 겪지 않을것이므로 참고만하자. 

```bash
File "/Users/a201808045/.pyenv/versions/3.7.0/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
  File "<frozen importlib._bootstrap>", line 983, in _find_and_load
  File "<frozen importlib._bootstrap>", line 967, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 677, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/Users/a201808045/github/TIL_Python/Django/django_study/mysite/mysite/urls.py", line 19, in <module>
    from my_app import urls
  File "/Users/a201808045/github/TIL_Python/Django/django_study/mysite/my_app/urls.py", line 7, in <module>
    path(r'get-url/', 'my_app.views.get_url', name='get-url'),
  File "/Users/a201808045/.virtualenv/django/lib/python3.7/site-packages/django/urls/conf.py", line 73, in _path
    raise TypeError('view must be a callable or a list/tuple in the case of include().')
TypeError: view must be a callable or a list/tuple in the case of include().
    path('my-app/', urls),
```

