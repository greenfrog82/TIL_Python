# 8. Function- and Class-Based Views

Django에는 Function-Based Views(FBVs)와 Class-Based Views(CBVs)가 있다. 여기서 이 둘에 대해서 이해해보도록 하자.  

## 8.1 When to Use FBVs or CBVs

view를 개발할 때, FBV 또는 CBV중 어떤 것을 선택해야하는지 늘 생각해야한다. 어떤 view는 CBV가 좋은 선택일 수 있고, 어떤 view는 FBV가 좋은 선택일 수 있다.   

다음은 FBV와 CBV 중 어떤 view를 선택할지에 대한 가이드라인이다. 

**CHECK**

가이드 라인을 보면 결국 CBV를 사용하되, 이를 통해 구현하기 어려울 경우 FBV를 선택하라고 되어있다. 그러면 CBV로 구현하기 어려울 정도로 복잡한 view가 FBV로 구현하면 정말 편해지는 경우가 존재하는가?

그러면서도 대부분의 view를 FBV로 개발하고 서브클래싱이 필요한 경우에만 CBV를 선택해도 된다고 되어있다. 우리는 어떻게 쓰고 있고, 어떻게 쓰는게 더 좋다고 생각하는지?
예를들어, 다음 두가지 항목으로 토의해볼 수 있겠다. 

* 가독성
* 재사용성

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

Example 8.1 참조 

**CHECK**

위 예제가 정말 잘못된 것인가? 우리도 이렇게 쓰는 경우가 있는데 ..
내 생각에 공통 코드에 파라미터를 달리해서 처리할 수 있는 view가 있다고 하면 이렇게 쓰는것도 괜찮아 보이는데?
책에 나오는 단점들도 잘 이해 안됨. 

