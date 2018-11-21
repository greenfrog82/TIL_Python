# [NullBooleanField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#nullbooleanfield)

`NullBooleanField`는 true, false, null값을 관리할 수 있는 필드이다. 공식문서에 보면, BooleanField(null=True)라는 설정을 쓰지말고 이를 쓰라고 되어있다.   

일단, 기존에 존재하던 `Person`모델에 `NullBooleanField`를 추가해보자.  

```python
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    try_to_travel = models.NullBooleanField()
```

이를 `makemigrations`한 후 `sqlmigrate`를 해보면 다음과 같다.   
쿼리를 보면 단순히 `bool NULL`속성을 주는것을 알 수 있다. 

```bash
$ ./manage.py sqlmigrate app_model 0002_person_try_to_travel
BEGIN;
--
-- Add field try_to_travel to person
--
ALTER TABLE "app_model_person" RENAME TO "app_model_person__old";
CREATE TABLE "app_model_person" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "try_to_travel" bool NULL, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL);
INSERT INTO "app_model_person" ("id", "first_name", "last_name", "try_to_travel") SELECT "id", "first_name", "last_name", NULL FROM "app_model_person__old";
DROP TABLE "app_model_person__old";
COMMIT;
```

`migrate`를 수행한 후 `shell_plus`를 통해 기존에 존재하던 데이터에 설정 된 `try_to_travel`값과 새로 생성 할 때 `try_to_travel`의 값을 설정하지 하지 않은 경우의 `try_to_travel`값을 확인해보자.  
이를 통해 `NullBooleanField`가 설정하는 기본값을 알 수 있다. 
확인 결과 `None` 타입이 기본값으로 설정되는것을 확인 할 수 있다.

```python
>>> Person.objects.all()
<QuerySet [<Person: Person object (1)>, <Person: Person object (2)>]>
>>> Person.objects.all()[0].try_to_travel
>>> Person.objects.all()[1].try_to_travel
>>> person = Person.objects.create(first_name='z', last_name='Z')
>>> person.first_name
'z'
>>> person.last_name
'Z'
>>> person.try_to_travel
>>> type(person.try_to_travel)
<class 'NoneType'>
```

## Questions 

여기서 궁금해지는 것이 있는데, `BooleanField(null=True)`인 경우 `sqlmigrate`를 통한 결과가 동일한가? 

우선 `Person`클래스를 다음과 같이 `BooleanField(null=True)`를 사용하는 형태로 수정하자.

```python
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    try_to_travel = models.BooleanField(null=True)
```

이를 `makemigrations`한 후 `sqlmigrate`를 통해 쿼리를 확인해보자. 
`create table`쿼리를 보면 `NullBooleanField`를 사용할 때와 동일한 것을 확인할 수 있다.  

```bash
$ ./manage.py sqlmigrate app_model 0005_auto_20181121_0316
BEGIN;
--
-- Alter field try_to_travel on person
--
ALTER TABLE "app_model_person" RENAME TO "app_model_person__old";
CREATE TABLE "app_model_person" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "try_to_travel" bool NULL, "first_name" varchar(30) NOT NULL, "last_name" varchar(30) NOT NULL);
INSERT INTO "app_model_person" ("id", "first_name", "last_name", "try_to_travel") SELECT "id", "first_name", "last_name", "try_to_travel" FROM "app_model_person__old";
DROP TABLE "app_model_person__old";
COMMIT;
```

`NoneBooleanField`와 같이 기존에 있던 데이터들을 확인해보고, `try_to_travel`의 값을 설정하지 않고 결과를 확인해보자. 
`NoneBooleanField`를 사용할 때와 동일하게 동작함을 알 수 있다. 

```bash
>>> Person.objects.all()
<QuerySet [<Person: Person object (1)>, <Person: Person object (2)>, <Person: Person object (3)>]>
>>> [person.try_to_travel for person in Person.objects.all()]
[None, None, None]
>>> person = Person.objects.create(first_name='HaHa', last_name='HoHo')
>>> person.try_to_travel
>>>
```

# Reference

* [Not using NullBooleanField](https://docs.quantifiedcode.com/python-anti-patterns/django/all/correctness/not_using_null_boolean_field.html)

