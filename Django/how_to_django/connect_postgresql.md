# How to connect PostgreSQL with Docker

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

>/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: \<http://initd.org/psycopg/docs/install.html#binary-install-from-pypi\>.

`psycopg2`를 사용하면 설치를 위해 소스코드를 빌드해야하고 또 이 빌드를 위해 필요로하는 것들이 있는데 더 이상 이러한 방법을 사용하지 말고 `wheel package`형태로 제공되는 psycopg2-binary`를 사용하라는 것이다. 따라서, 앞서 설치했던 `psycopg2`를 삭제하고 `psycopg2-binary`를 설치하도록 하자.  

```sh
$ pip uninstall psycopg2
Uninstalling psycopg2-2.7.6.1:
  Would remove:
    /Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/psycopg2-2.7.6.1.dist-info/*
    /Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/psycopg2/*
Proceed (y/n)? y
  Successfully uninstalled psycopg2-2.7.6.1
$ pip install psycopg2-binary
Collecting psycopg2-binary
  Using cached https://files.pythonhosted.org/packages/fe/df/933e81c7fa95a915a9d67bd5736963a99513568f82cfc937c76d0d6f3414/psycopg2_binary-2.7.6.1-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl
Installing collected packages: psycopg2-binary
Successfully installed psycopg2-binary-2.7.6.1
```

## How to interact with PostgreSQL on Docker

### Usign Docker

`Docker`를 통해 띄어놓은 `PostgreSQL`에 접속하기 위해서는 다음 명령을 사용하면 된다.  

>$ docker exec -it \<container name\> psql -U \<psql user name\>

그럼 현재 실행중인 `Docker`에 띄어놓은 `PostgreSQL`에 접속해보자.  

```sh
docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                                                                                        NAMES
d14102035ae6        adminer               "entrypoint.sh docke…"   4 days ago          Up 4 days           0.0.0.0:8080->8080/tcp                                                                       til_python_adminer_1
602f294aaff9        postgres              "docker-entrypoint.s…"   5 days ago          Up 4 days           0.0.0.0:5432->5432/tcp                                                                       greenfrog-postresql-how-to-django
779538d46e70        rabbitmq:management   "docker-entrypoint.s…"   5 days ago          Up 4 days           4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp   greenfrog-rabbitmq
234aed277e9a        redis:latest          "docker-entrypoint.s…"   5 days ago          Up 4 days           0.0.0.0:6379->6379/tcp                                                                       greenfrog-redis
bf57a246b77f        memcached:latest      "docker-entrypoint.s…"   5 days ago          Up 4 days           0.0.0.0:11211->11211/tcp                                                                     greenfrog-memcached
$
$ docker exec -it 602f294aaff9 psql -U postgres psql (11.1 (Debian 11.1-1.pgdg90+1))
Type "help" for help.

postgres=# \d+
                                      List of relations
 Schema |               Name                |   Type   |  Owner   |    Size    | Description
--------+-----------------------------------+----------+----------+------------+-------------
 public | app_model_article                 | table    | postgres | 8192 bytes |
 public | app_model_article_id_seq          | sequence | postgres | 8192 bytes |
 public | app_model_person                  | table    | postgres | 0 bytes    |
 public | app_model_person_id_seq           | sequence | postgres | 8192 bytes |
 public | app_model_point                   | table    | postgres | 0 bytes    |
 public | app_model_point_id_seq            | sequence | postgres | 8192 bytes |
 public | app_model_userprofile             | table    | postgres | 0 bytes    |
 public | app_model_userprofile_id_seq      | sequence | postgres | 8192 bytes |
 public | auth_group                        | table    | postgres | 0 bytes    |
 public | auth_group_id_seq                 | sequence | postgres | 8192 bytes |
 public | auth_group_permissions            | table    | postgres | 0 bytes    |
 public | auth_group_permissions_id_seq     | sequence | postgres | 8192 bytes |
 public | auth_permission                   | table    | postgres | 8192 bytes |
 public | auth_permission_id_seq            | sequence | postgres | 8192 bytes |
 public | auth_user                         | table    | postgres | 8192 bytes |
 public | auth_user_groups                  | table    | postgres | 0 bytes    |
 public | auth_user_groups_id_seq           | sequence | postgres | 8192 bytes |
 public | auth_user_id_seq                  | sequence | postgres | 8192 bytes |
 public | auth_user_user_permissions        | table    | postgres | 0 bytes    |
 public | auth_user_user_permissions_id_seq | sequence | postgres | 8192 bytes |
 public | django_admin_log                  | table    | postgres | 8192 bytes |
 public | django_admin_log_id_seq           | sequence | postgres | 8192 bytes |
 public | django_content_type               | table    | postgres | 8192 bytes |
 public | django_content_type_id_seq        | sequence | postgres | 8192 bytes |
 public | django_migrations                 | table    | postgres | 16 kB      |
 public | django_migrations_id_seq          | sequence | postgres | 8192 bytes |
 public | django_session                    | table    | postgres | 8192 bytes |
(27 rows)

postgres=#
```

### Using dbshell

Django는 `DATABASES`설정에 연결된 데이터베이스에 접근하기 위한 툴로 `dbshell`이라는 command를 제공한다. 이에 대한 자세한 내용은 다음 링크를 참고하도록 하자.  

[Django - dbshell command](https://github.com/greenfrog82/TIL_Python/blob/master/Django/how_to_django/dbshell_command.md)

위 문서를 읽어보면, 일단 `PostgreSQL`에서 `dbshell command`를 사용하려면 로컬에 `psql`이 설치되어 있어야한다. 결국 `PostgreSQL`을 로컬에 설치하기 싫어서 `Docker`에 올린건데;; 이거 참 ...

일단 다음과 같이 로컬에 `PostgreSQL`을 설치하자. 

```sh
$ brew install postgresql
```

`PostgreSQL` 설치가 완료됐으면 `dbshell command`를 통해 `Docker`를 통해 올려놓은 `PostgreSQL`에 접속해보자.  

```sh
./manage.py dbshell
psql (11.1)
Type "help" for help.

postgres=# \d+
                                      List of relations
 Schema |               Name                |   Type   |  Owner   |    Size    | Description
--------+-----------------------------------+----------+----------+------------+-------------
 public | app_model_article                 | table    | postgres | 8192 bytes |
 public | app_model_article_id_seq          | sequence | postgres | 8192 bytes |
 public | app_model_person                  | table    | postgres | 0 bytes    |
 public | app_model_person_id_seq           | sequence | postgres | 8192 bytes |
 public | app_model_point                   | table    | postgres | 0 bytes    |
 public | app_model_point_id_seq            | sequence | postgres | 8192 bytes |
 public | app_model_userprofile             | table    | postgres | 0 bytes    |
 public | app_model_userprofile_id_seq      | sequence | postgres | 8192 bytes |
 public | auth_group                        | table    | postgres | 0 bytes    |
 public | auth_group_id_seq                 | sequence | postgres | 8192 bytes |
 public | auth_group_permissions            | table    | postgres | 0 bytes    |
 public | auth_group_permissions_id_seq     | sequence | postgres | 8192 bytes |
 public | auth_permission                   | table    | postgres | 8192 bytes |
 public | auth_permission_id_seq            | sequence | postgres | 8192 bytes |
 public | auth_user                         | table    | postgres | 8192 bytes |
 public | auth_user_groups                  | table    | postgres | 0 bytes    |
 public | auth_user_groups_id_seq           | sequence | postgres | 8192 bytes |
 public | auth_user_id_seq                  | sequence | postgres | 8192 bytes |
 public | auth_user_user_permissions        | table    | postgres | 0 bytes    |
 public | auth_user_user_permissions_id_seq | sequence | postgres | 8192 bytes |
 public | django_admin_log                  | table    | postgres | 8192 bytes |
 public | django_admin_log_id_seq           | sequence | postgres | 8192 bytes |
 public | django_content_type               | table    | postgres | 8192 bytes |
 public | django_content_type_id_seq        | sequence | postgres | 8192 bytes |
 public | django_migrations                 | table    | postgres | 16 kB      |
 public | django_migrations_id_seq          | sequence | postgres | 8192 bytes |
 public | django_session                    | table    | postgres | 8192 bytes |
(27 rows)

postgres=#
```

## Where to store data

앞선과정을 통해서 `Docker`에 `PostgreSQL`을 올려서 Django와 연동을 해두었지만, 데이터가 `Docker Container`내부에 있기 때문에 `Docker`를 삭제하고 나면 데이터가 유지되지 않는다. 따라서 데이터를 유지하기 위해서는 호스트 PC와 `volume`으로 연결해주어야한다.  

이를위해 우선 `docker-compose.yml`파일을 열어서 `volume`설정을 해주도록 하자. `PostgreSQL`은 `PGDATA`환경변수를 통해 경로를 지정해주지 않으면 기본적으로 `/var/lib/postgresql/data`에 데이터 저장한다. 따라서 호스트 PC의 적당한 위치와 `/var/lib/postgresql/data`를 `volume`으로 묶어주자. 

```yaml
version: '3'
services:
    db:
        container_name: greenfrog-postresql-how-to-django
        image: postgres
        restart: always
        volumes: 
            - /var/lib/postgresql/data
        ports:
            - 5432:5432
    adminer:
        image: adminer
        restart: always
        ports:
            - 8080:8080
```

이제 기존`Docker Container`를 삭제한 후 다시 실행해주자.  

```sh
$ docker-compose stop -t 0
Stopping greenfrog-postresql-how-to-django ... done
Stopping til_python_adminer_1              ... done
Stopping greenfrog-rabbitmq                ... done
Stopping greenfrog-redis                   ... done
Stopping greenfrog-memcached               ... done
$
$ docker-compose rm
Going to remove greenfrog-postresql-how-to-django, til_python_adminer_1, greenfrog-rabbitmq, greenfrog-redis, greenfrog-memcached
Are you sure? [yN] y
Removing greenfrog-postresql-how-to-django ... done
Removing til_python_adminer_1              ... done
Removing greenfrog-rabbitmq                ... done
Removing greenfrog-redis                   ... done
Removing greenfrog-memcached               ... done
$
$ docker-compose up -d
Creating greenfrog-memcached               ... done
Creating til_python_adminer_1              ... done
Creating greenfrog-postresql-how-to-django ... done
Creating greenfrog-redis                   ... done
Creating greenfrog-rabbitmq                ... done
```

`Docker Container`를 삭제한 후 다시 실행했기 때문에 앞서 `migrate`했던 데이터들은 모두 삭제되었을것이다. 이를 확인해보자.  

```sh
./manage.py dbshell
psql (11.1)
Type "help" for help.

postgres=# \d
Did not find any relations.
postgres=# \d+
Did not find any relations.
```

앞서 `migrate`했던 데이터들이 모두 삭제된것을 확인할 수 있다. 다시 한번 `migreate`명령을 수행해주자.  

```sh
./manage.py migrate
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

이제 다시 `Docker Container`를 삭제했다 다시 올리더라도 데이터가 유지되는것을 확인 할 수 있다. 

# Reference

* [DockerHub - postgres](https://hub.docker.com/_/postgres)
* [psycopg](http://initd.org/psycopg/)
* [dbshell](https://docs.djangoproject.com/en/2.1/ref/django-admin/#dbshell)
* [How to interact with your project’s database](https://docs.divio.com/en/latest/how-to/interact-database.html)