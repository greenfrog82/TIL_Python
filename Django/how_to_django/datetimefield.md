# [DateTimeField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#datetimefield) and [DateField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield)

```python
class DateTimeField(auto_now=False, auto_now_add=False, **options)
class DateField(auto_now=False, auto_now_add=False, **options)
```

# Description

* `DateTimeField`는 날짜와 시간을 표현하는 필드로 Python의 datetime.datetime 인스턴스로 표현된다. 
* `DateField`는 날짜를 표현하는 필드로 Python의 datetime.date 인스턴스로 표현된다.

앞서 설명한 것과 같이 `DateTimeField`와 `DateField`는 각각 날짜와 시간 그리고 날짜를 표현한다는 것을 제외하면 전달 받는 파라메터들과 동작이 동일하다.  
따라서, 본 문서에서는 `DateTimeFiled`만을 설명한다.  

# Parameters

## auto_now

auto_now의 값이 True인 경우, 모델이 저장될 때 현재시간으로 필드의 값을 업데이트한다. 따라서, '최근 변경시간'을 기록하기 위해서 유용하게 사용할 수 있다.  

해당 필드의 값은 Model.save() 메소드가 호출될 때만 자동으로 업데이트되며, QuerySet.update()를 통해 다른 필드를 수정했을 때는 업데이트되지 않는다. (? 왜 이렇게 디자인해놨을까? QuerySet.update()를 통해 특정 필드만 수정했다하더라도 모델은 업데이트되는 것인데 ...) 하지만, QuerySet.update()를 통해 해당 필드를 수정한다면 수정된다.

**Note**

auto_now의 값이 True로 설정되어 있다고 해당 필드의 값을 수정할 수 없는 것은 아니다. 단지, 수정을 했더라도 Model.save() 메소드가 호출 될 때의 시간으로 업데이트 되기 때문에 필드의 값을 수정하는 것이 의미가 없을 뿐이다. 

## auto_now_add

`auto_now_add`의 값이 True인 경우, 모델이 **최초로 저장**될 때 현재시간을 필드의 값으로 저장한다. 따라서, '최초 생성시간'을 기록하기 위해서 유용하게 사용할 수 있다.  

`auto_now_add`의 동작이 좀 재미있는 부분이 있는데 모델을 생성할 때, 해당 속성이 들어간 필드의 값을 설정해줬다고 하더라도 `save()`함수를 호출하는 시점에 해당 시간으로 바뀐다는 것이다.  
만약, 해당 속성이 들어간 필드의 값을 설정하여 저장을 하고 싶고 만약 필드값을 설정하지 않은 경우 `default`값이 필요하다고 하면 `auto_now_add`속성이 아닌 `default`속성을 사용하는것이 바람직하다.  
`default`값을 설정할 때는 다음을 참고자하자. 

* DateTimeField의 경우 `default=django.utils.timezone.now`를 설정하고, 
* DateField의 경우 `default=django.date.today`를 설정하자.

**Note**

auto_now_add의 값이 True인 경우라도 해당 필드의 값은 언제든지 수정 될 수 있다.

# Example

에제를 진행하기 앞서 다음과 같은 모델을 정의하자.  
우선 각각 `auto_now_add`과 `auto_now`를 True로 설정했을 때 동작을 알아보기 위해 해당 옵션을 설정하였다. 

```python
from django.db import models

class Article(models.Model):
    contents = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
```

Django shell에서 다음과 같이 Article 객체를 생성한 후 'test'라는 값을 설정한 후 저장해보자.  
Article 객체를 최초 생성한 것이기 때문에 `created_date`와 `updated_date`의 값이 동일하다. 

```python
>>> from app_model.models import Article
>>> obj = Article()
>>> obj.contents = 'test'
>>> obj.save()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 40, 19, 46442, tzinfo=<UTC>)
>>> obj.updated_date
datetime.datetime(2018, 9, 27, 23, 40, 19, 46680, tzinfo=<UTC>)
```

이제 해당 객체의 contents 필드의 값을 'A'로 수정한 후 다시 저장해보자.  
`created_date`는 변경이 없지만, `updated_date`는 업데이트 된것을 알 수 있다.  

```python
>>> obj.contents = 'A'
>>> obj.save()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 40, 19, 46442, tzinfo=<UTC>)
>>> obj.updated_date
datetime.datetime(2018, 9, 27, 23, 41, 9, 820278, tzinfo=<UTC>)
```

앞서 `auto_now` 파라메터를 소개 할 때 `QuerySet.update()`를 통해 다른 필드의 값을 변경했을 때는 해당 필드의 값이 변경되지 않는다는 설명을 했었다. 
이를 확인해보자. 다음과 같이 contents가 'A'인 데이터를 찾아서 'B'로 변경한 후 update() 메소드를 호출하였다. 

앞서 설명헀던대로 `updated_date`는 `QuerySet.update()`를 통해 다른 필드의 값을 변경했을 때는 해당 필드의 값은 변경되지 않는것을 확인할 수 있다.

```python
>>> Article.objects.filter(contents='A').update(contents='B')
1
>>> obj = Article.objects.filter(contents='B').first()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 40, 19, 46442, tzinfo=<UTC>)
>>> obj.updated_date
datetime.datetime(2018, 9, 27, 23, 41, 9, 820278, tzinfo=<UTC>)
```

이번에는 `QuerySet.udpate()`를 통해 `updated_date`를 수정해보자.  
이 경우에는 `updated_date`의 값이 변경됨을 알 수 있다.   

```python
>>> from django.utils import timezone
>>> Article.objects.filter(contents='B').update(updated_date=timezone.now())
1
>>> obj = Article.objects.filter(contents='B').first()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 40, 19, 46442, tzinfo=<UTC>)
>>> obj.updated_date
datetime.datetime(2018, 9, 27, 23, 43, 6, 850024, tzinfo=<UTC>)
```

앞서 `auto_now_add` 파라메터를 소개할 때 최초 객체가 생성될 때 해당 필드의 값을 설정하여도 객체가 저장되면 설정한 값이 무시되고 현재 시간이 설정된다고 설명한적이 있다.   
이를 확인해보자. Article 객체를 생성한 후 `created_date`에 임의의 값을 설정한 후 객체를 저장해보았다.  
다음과 같이 객체가 저장될 때 `created_date`에 설정했던 값이 무시되고 저장 될 때의 시간이 설정된 것을 확인 할 수 있다. 

```python
>>> obj = Article()
>>> obj.created_date = 'test'
>>> obj.save()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 43, 59, 697220, tzinfo=<UTC>)
>>> obj.updated_date
datetime.datetime(2018, 9, 27, 23, 43, 59, 697274, tzinfo=<UTC>)
```

`auto_now_add` 파라메터가 True로 설정되어 있다고 하더라도 해당 필드의 값을 변경할 수 있기 때무에 주의해야한다.  
앞서 생성한 예제에 이어 obj객체의 created_date 필드의 값을 수정해보자. 수정이 정상적으로 이루어지는 것을 확인 할 수 있다. 

```python
>>> obj.created_date = timezone.now()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 59, 25, 318455, tzinfo=<UTC>)
>>> obj.save()
>>> obj.created_date
datetime.datetime(2018, 9, 27, 23, 59, 25, 318455, tzinfo=<UTC>)
>>> obj.updated_date
datetime.datetime(2018, 9, 27, 23, 59, 30, 418160, tzinfo=<UTC>)
```

이와같이 `auto_now_add` 속성을 사용하면 의도치 않은(?) 문제가 발생할 수 있으므로, 모델이 생성되는 시점에 날짜가 기록되야하는 경우가 아닌 겨우라면 `default`속성을 사용하라고 했었다.  
이를 확인해보자. 우선 다음과 같은 모델이 있다고 가정하자.  

```python
from django.utils import timezone

class DateTimeTestModel(models.Model):
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True)
```

이제 앞선 예제와 같이 모델을 생성한 후 `started_at`속성에 날짜를 할당한 후 `save()`함수를 호출해보면, `auto_now_add`때와는 달리 달리 `started_at`속성에 할당해두었던 값이 저장된것을 알 수 있다. 

```python
>>> from django.utils import timezone
>>> from datetime import timedelta
>>> started_at = timezone.now() + timedelta(days=10)
>>> started_at
datetime.datetime(2019, 1, 20, 1, 7, 41, 595928, tzinfo=<UTC>)
>>> tt = DateTimeTestModel()
>>> tt.started_at = timezone.now() + timedelta(days=10)
>>> tt.save()
>>> dt = DateTimeTestModel.objects.first()
>>> dt.started_at
datetime.datetime(2019, 1, 20, 1, 7, 41, 595928, tzinfo=<UTC>)
```

# Reference

* [auto_now VS auto_now_add](http://tomining.tistory.com/145)
* [DateField.auto_now](https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.DateField.auto_now)
* [DateField.auto_now_add](https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.DateField.auto_now_add)
