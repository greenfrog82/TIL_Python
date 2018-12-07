# 9. Best Practices for Function-Based Views

Django로 프로젝트를 시작한 이래로, `FBV`는 전 세계의 개바자들로부터 주로 사용되고있다. `CBV`의 사용량이 증가하고 있지만, `FBV`의 사용성에 대한 단순함은 Django 초보과 경험자 모두에게 매력적이다. Two scoop의 저자는 `CBV`를 선호하지만, 프로젝트를 진행하면서 `FBV`을 잘 사용할 수 있는 방법에 대해서 소개한다.   

## 9.1 Advantages of FBVs

`FBV`의 단순함은 코드의 재사용을 포기한 결과이다. `FBV`는 `CBV`와 같이 부모 클래스의 기능을 상속하여 코드를 재사용할 수 없다. `FBV`는 분명히 기능적이라는 장점을 가지고 있고, 이러한 면은 몇가지 흥미로운 전략을 이끌어낸다.  

`FBV`를 사용할 때, 다음 가이드를 따르자. 

* view 코드는 간단하고 코드량이 적어야한다.
* 반복되지 않는 코드가 view에 존재해야한다. 
* **?** view는 화면 단 로직만 핸들링해야한다. 가능한 비즈니스 로직은 model에 있거나, 반드시 form에 있어야한다.  
* 커스텀 403, 404 그리고 500 에러 핸들러를 작성할 때 사용해라. 
* 복잡한 중첩 된 if문의 사용은 피해라. 

## 9.2 Passing the HttpRequest Object

`middleware` 또는 `context processor`와 같은 모든 요청에 공통적으로 적용되는 로직이 아닌, 특정 view에서 재사용되기위한 코드를 작성해보자. 책의 시작에서 우리는 이미 `유틸리티 함수`를 작성하라고 가이드 했었다.  

대부분의 `유틸리티 함수`는 django.http.HttpRequest(이하 HttpRequest)의 속성 또는 속성들을 인자로 사용한다. 사실 `유틸리티 함수`가 전달받아야하는 핵심 파라메터는 HttpRequest 하나이다. HttpRequest로부터 필요한 속성들을 선택해서 `유틸리티 함수`를 작성하면 함수 시그니처가 복잡해져서 오히려 가독성이 떨어진다.  
따라서, **HttpRequest 하나만 유틸리티 함수의 인자로 전달하도록 하자. 물론 HttpRequest로 부터 전달해야하는 인자가 아니라면 추가적을 전달해야하는것은 반드시 필요하다.**

예를들어, 어떤 권한이 부여되었는지 여부를 결정하는 기능있다고하자. 이러한 기능은 여러 함수에서 재사용될 수 있으니 다음과 같이 `유틸리티 함수`로 분리해두면 재사용성이 높아질 것이다. 이때 `유틸리티 함수`의 인자로 `HttpRequest`를 전달하도록 하자. 

```python
from django.core.exceptions import PermissionDenide

def check_sprinkle_rights(request):
    if request.user.can_sprinkle or request.user.is_staff:
        request.can_sprinkle = True
        return request

    raise PermissionDenied
```

이제 위 함수를 sprinkle 목록을 출력하거나 상세를 보여주기위한 view에서 호출하므로서 로직을 재사용할 수 있게 되었다.  
```python
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .utils import check_sprinkles
from .models import Sprinkle

def sprinkle_list(request):
    request = check_sprinkles(request)
    
    return render(request,
        'sprinkles/sprinkle_list.html',
        {'sprinkels': Sprinkle.objects.all()})

def sprinkle_detail(request, pk):
    request = check_sprinkles(request)

    sprinke = get_object_or_404(Sprinkle, pk=pk)

    return render(request, 
        'sprinkles/sprinkle_detail_html',
        {'sprinkle': sprinkle})
```

사실 앞서 작성한 `유틸리티 함수`의 성격은 특정 view별로 동작해야하는 `middleware`와 같다. 이러한 경우 `decorator`를 이용하는것이 가독성을 높이고 view와 로직을 분리할 수 있어서 좋다. 

## 9.3 Decorators Are Sweet

**syntactic sugar**는 로직을 좀 더 읽기 쉽게하거나 표현하게 하기위해 프로그래밍 언어에 추가되는 문법이다. 파이썬에서 `decorator`는 이러한 용도로 추가된 기능이다. 

데코레이터의 사용법은 다음 링크 참조. 

[How to use Decorator](https://github.com/greenfrog82/TIL_Python/tree/master/Basic/decorators/basic)

## 9.3.1 Be Conservative With Decorators

`decorator`가 중첩되면, 마치 상속을 복잡하게 한것과 같이 코드의 가독성이 떨어지게 된다. 따라서 view에 사용할 `decorator`의 수를 적절히 제한할 필요가 있다. 

## 9.4 Passing the HttpResponse Object


