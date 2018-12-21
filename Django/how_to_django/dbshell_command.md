# [dbshell](https://docs.djangoproject.com/en/2.1/ref/django-admin/#dbshell)

>$ ./manage.py dbshell

`settings.py`의 `DATABASES`설정의 `ENGINE`에 명시된 데이터베이스 엔진을 위한 command line 클라이언트 툴을 실행시킨다. 설정은 다음 코드를 참고하자. 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.PostgreSQL',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

각각 데이터베이스 엔진에 따라 실행시키는 command line 툴은 각각 다음과 같다.  

* PostgreSQL : psql
* MySQL : mysql
* SQLite : sqlite3
* Oracle : sqlplus

`dbshell` command는 앞서 소개한 command line 툴들이 호출될 수 있는 옳바른 경로에 설치되어있다고 가정한다. command line 툴에 대한 경로를 명시할 수 없다는것을 주의하자.  

`settings.py`의 `DATABASES`설정에 데이터베이스는 여러개가 설정될 수 있다. 따라서 설정 된 여러개의 데이터베이스 중 하나를 선택할 수 있는데 `--database`옵션과 함께 데이터베이스 이름을 전달하면된다. 만약 해당 옵션을 주지 않으면 `default`데이터베이스가 선택된다.   
다음은 해당 옵션의 사용방법이다.  

>$ ./manage.py dbshell --database \<database name\>
