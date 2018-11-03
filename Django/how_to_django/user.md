# User objects

## Creating users

Django에서 User instance를 생성하는 가장 직접적인 방법은 User 모델의 `create_user` 메소드를 사용하는 것이다.   

```python
>>> user = User.objects.create_user('username', 'email@email.com', 'password')
>>> user.username
'username'
>>> user.email
'email@email.com'
>>> user.password
'pbkdf2_sha256$120000$l9yuBSEv2okO$b25o/GriaQSS5j5FJihlHUC0Q3xQppMrt+NZPeDXz3E='
>>> user.is_active
True
>>> user.is_staff
False
>>> user.is_superuser
False
```

## Creating superusers

Superuser를 생성할 수 있는 방법은 일반 User를 생성할 때와 같이 `create_superuser` 메소드를 호출하는 방법과 `createsuperuser` command를 사용하는 방법 두 가지가 있다. 

### Using create_superuser method 

`create_superuser` 메소드는 User 모델의 `is_staff`와 `is_superuser` 속성에 **True**를 설정해주는것을 제외하면 `create_user` 메소드와 동일하다.  
참고로 `create_user` 메소드는 `is_staff`와 `is_superuser` 속성을 **False**로 설정한다.

```python
>>> superuser = User.objects.create_superuser('superuser', 'superuser@email.com', 'password')
>>> superuser.username
'superuser'
>>> superuser.email
'superuser@email.com'
>>> superuser.password
'pbkdf2_sha256$120000$o7dHVNNo0mE8$/x78XwCu0lUPnZ6FTPYq9cFncRyw/1RsRJmOd1FythE='
>>> superuser.is_active
True
>>> superuser.is_staff
True
>>> superuser.is_superuser
True
```




## Reference

* [User objects](https://docs.djangoproject.com/en/2.1/topics/auth/default/#user-objects)
* [create_user](https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user)
* 

