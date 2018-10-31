# [Proxy](https://docs.djangoproject.com/en/2.1/topics/db/models/#proxy-models)

`Proxy 모델 상속`은 오직 모델에 대한 파이썬 코드의 동작을 변경하기를 원할 때 사용할 수 있다.  
`Proxy 모델 상속`은 원본 모델의 Proxy를 만든다. 이렇게 생성 된 Proxy를 통해 마치 원본 모델에 데이터를 생성, 삭제 그리고 업데이트하듯이 데이터를 다룰 수 있다.  
`Proxy 모델 상속`을 통해 원본 모델의 변경 없이 원본 모델의 ordering을 변경하거나 기본 Manager를 변경하는 등 원본 모델에 정의된 동작과 다른 동작을 원본 모델에 적용할 수 있다.  

Proxy 모델 상속은 일반적인 모델을 정의하는 방법과 동일하다. 단, `Meta`클래스의 `Proxy` 속성에 `True`를 설정해주면 된다.  

다음 예제를 보자.  
`Person`모델이 원본 모델이 `MyPerson`이라는 `Proxy Model`을 작성하였다.  

```python
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class MyPerson(Person):
    class Meta:
        proxy = True
```

이를 `migrate`한 후 DB에 테이블이 어떻게 생성되었나 확인해보자.  
다음과 같이 `Person` 모델에 대응하는 `app_model_person` 테이블은 존재하지만, `MyPerson` 모델에 대응하는 테이블은 찾을 수 없다.  
`Proxy 모델 상속`은 실제 테이블을 생성하지 않고, Proxy를 통해 하나의 테이블을 공유한다. 

```sql
sqlite> .tables
app_model_article           auth_user
app_model_person            auth_user_groups
app_model_point             auth_user_user_permissions
app_model_userprofile       django_admin_log
auth_group                  django_content_type
auth_group_permissions      django_migrations
auth_permission             django_session
```

앞서 Proxy를 통해 하나의 테이블을 공유한다고 했다. 정말 그런지 확인해보자.  
다음 예제를 보면, `Person`을 통해서 생성한 데이터를 `MyPerson`을 통해서 접근하고, 반대의 경우도 잘 동작함을 알수 있다. 

```python
>>> Person.objects.all()
<QuerySet []>
>>> Person.objects.create(first_name='a', last_name='A')
<Person: Person object (1)>
>>> MyPerson.objects.all()[0]
<MyPerson: MyPerson object (1)>
>>> MyPerson.objects.all()[0].first_name
'a'
>>> MyPerson.objects.all()[0].last_name
'A'
>>> MyPerson.objects.create(first_name='b', last_name='B')
>>> Person.objects.all()
<QuerySet [<Person: Person object (1)>, <Person: Person object (2)>]>
>>> Person.objects.all()[1].first_name
'b'
>>> Person.objects.all()[1].last_name
'B'
```

예를들어, 조회를 할 때 `last_name`을 통해 내림차순으로 정렬되는 전용 모델을 만들고 싶은 경우 역시 `Proxy 모델`을 사용할 수 있다.  
다음과 같이 `Proxy 모델`을 정의해보자.  

```python
class OrderedPerson(Person):
    class Meta:
        ordering = ['-last_name']
        proxy = True
```

위 모델을 통해 다시 데이터를 생성한 후 `Person`모델을 통해 조회를 해보고 `OrderedPerson`모델을 통해 조회를해보자.  
`Person`모델은 오름차순으로 정렬을하고, `OrderedPerson`모델은 내림차순으로 정렬이 되는것을 알 수 있다. 

```python
>>> Person.objects.all()
<QuerySet []>
>>> Person.objects.create(first_name='a', last_name='A')
<Person: Person object (1)>
>>> Person.objects.create(first_name='b', last_name='B')
<Person: Person object (2)>
>>> Person.objects.all()
<QuerySet [<Person: Person object (1)>, <Person: Person object (2)>]>
>>> OrderedPerson.objects.all()
<QuerySet [<OrderedPerson: OrderedPerson object (2)>, <OrderedPerson: OrderedPerson object (1)>]>
```

그럼 `Proxy 모델`에 필드를 추가하면 어떻게 될까?   
다음과 같이 `MyPerson`에 `age` 필드를 추가해보자. 

```python
class MyPerson(Person):
    age = models.PositiveIntegerField()
    
    class Meta:
        proxy = True
```

이제 `makemigrations`명령을 실행하면 다음과 같이 `Proxy 모델`에는 필드를 추가할 수 없다는 에러 메시지가 출력된다. 

```bash
$ ./manage.py makemigrations
SystemCheckError: System check identified some issues:

ERRORS:
?: (models.E017) Proxy model 'MyPerson' contains model fields.
```

