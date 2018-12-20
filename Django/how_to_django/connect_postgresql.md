# How to connect PostgreSQL

>* macOS Mojave version 10.14.2
>* Python 3.7.0
>* Django 2.1
>* Docker Desktop Version 2.0.0.0-mac81 (29211)
>* PostgreSQL

본 문서에서는 `Django 2.1`에 `Docker`를 통해 실행시킨 `PostgreSQL`을 연동하는 방법에 대해서 설명한다.

## Adding PostgreSQL to services of docker-composer

`PostgreSQL`을 `docker-composer`의 서비스에 등록하자.  
`adminer`의 경우 PHP로 개발되어 웹으로 서비스되는 데이터베이스 관리 툴이다. 

```yaml
version: '3'
services:
    db:
        container_name: greenfrog-postresql-how-to-django
        image: postgres
        restart: always
        ports:
        - 5432:5432
    adminer:
        image: adminer
        restart: always
        ports:
        - 8080:8080
```

다음 명령을 통해 `docker-compose`를 실행시키자.   

```sh
$ docker-compose up -d
```

이제 웹 브라이우저를 통해 `adminer`에 접속하여 `http://localhost:8080`로 접속해서 아이디/패스워드를 넣으면 `docker-compose`를 통해 실행 된 `PostgreSQL`에 접근할 수 있다. 기본 아이디/패스워드는 `postgres/postgres`이다.  

## Set up PostgreSQL in Django

`settings.py`파일을 열어서 `DATABASES`속성을 다음과 같이 수정하자. 

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

## Migrating DB

이제 데이터베이스를 변경했으니, 기존 데이터베이스를 마이그레이션하도록 하자.  
이를 위해 다음과 같이 명령을 수행하면, 에러가 발생한다.  

```sh
$ ./manage.py migrate
Traceback (most recent call last):
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/backends/PostgreSQL/base.py", line 20, in <module>
    import psycopg2 as Database
ModuleNotFoundError: No module named 'psycopg2'
```

위 에러는 `psycopg2`모듈이 설치되어 있지 않아서 발생한 문제이다. `psycopg2`는 `Python`에서 `PostgreSQL`을 사용하기 위한 `DataBase Adapter`로 이 모듈이다. 때문에 해당 모듈이 없다면, `Django`는 `PostgreSQL`를 통해 어떠한 작업도 할 수 없다.  
다음 명령을 통해 `psycopg2`를 설치하자.  

```sh
$ pip install psycopg2
```

이제 다시 마이그레이션을 수행해보자. 마이그레이션이 정상적으로 수행되는것을 확인 할 수 있다. 

```sh
$ ./manage.py migrate
/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
  """)
Operations to perform:
  Apply all migrations: admin, app_model, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying app_model.0001_initial... OK
  Applying app_model.0002_person_try_to_travel... OK
  Applying app_model.0003_compareperson... OK
  Applying app_model.0004_auto_20181121_0313... OK
  Applying app_model.0005_auto_20181121_0316... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK
```

그런데 마이그레이션 과정에서 다음과 같이 경고 메시지가 출력되었다. 이건 뭘까?

>Psycopg is the most popular PostgreSQL adapter for the Python programming language. At its core it fully implements the Python DB API 2.0 specifications. Several extensions allow access to many of the features offered by PostgreSQL.

# Reference

* [DockerHub - postgres](https://hub.docker.com/_/postgres)
* [psycopg](http://initd.org/psycopg/)