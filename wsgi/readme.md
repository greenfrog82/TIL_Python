# How to set up NginX, uWSGI and Django

## Concept

Django를 통해 웹 서비스를 구축하기 위해서는 다음 항목들이 필요하다. 

1. 웹 서버(NginX)
2. Web Server Gateway Interface(WSGI), uWSGI
3. Django Server

앞서 설명한 3개의 어플리케이션들은 다음과 같이 Request를 받아 Response를 전달한다.  

>Client <-> Web Server <-> Socket <-> uWSGI <-> Django 

### 1. 웹 서버(NginX)

HTML, Images, CSS 등 정적 파일을 서빙하고 `Reverse Proxy`, `Security` 처리등을 한다. 또한 `uWSGI` 프로세스와 소켓 통신을 통해 클라이언트의 요청을 Django Server로 전달한다.  

### 2. Web Server Gateway Interface(WSGI), uWSGI

`WSGI`는 파이썬의 표준으로 파이썬이 어플리케이션이 웹 서버로부터 클라이언트의 Request를 전달받아 서버의 Response를 전달하기 위한 규약이다.   
`uWSGI`는 이 규약을 구현한 구현체이다.   

### 3. Django Server 

Django를 통해 개발한 웹 어플리케이션 서버이다.  

## Before you start setting up uWSGI

uWSGI를 설치하고 설정하기 전에 먼저 `virtualenv`를 생성한 후, `Django`를 통해 프로젝트를 생성하자.   
각각 다음 링크를 참조하자.  

* [virtualenv, virtualenvwrapper and pyenv](https://github.com/greenfrog82/TIL_Python/tree/master/Basic/virtualenv_virtualenvwrapper_pyenv)
* [How to start Django project](https://github.com/greenfrog82/TIL_Python/tree/master/Django/how_to_start_django_project)

## Basic uWSGI installation and Configuration

여기서는 uWSGI를 설치하고 간단히 설정하는 방법에 대해서 알아보자. 

### install uWSGI into your virtualenv

>$ pip install uwsgi

### Basic test

다음과 같이 [test.py](./test.py)을 만들자. 해당 파일은 uwsgi 모듈이 요청을 받아서 처리하기 위한 파이썬 어플리케이션이다. 

```python
def application(env, start_response):
    start_response('200 OK', [('Context-Type', 'text/html')])
    return [b'Hello World'] # Python3
    # return ['Hello World'] # Python2
```

앞서 작성한 파이썬 어플리케이션을 `uwsgi`를 통해 실행시켜보자.  

>$ uwsgi --http :8000 --wsgi-file test.py

위에 사용된 옵션은 다음과 같다.  

* `http :8000` : http 프로토콜을 사용하고 8000번 포트를 사용한다. 
* `wsgi-file test.py` : 파이썬 어플리케이션(test.py)을 지정한다. 

실행이 된 모습은 다음과 같다. 

```sh
$ uwsgi --http :8000 --wsgi-file test.py
*** Starting uWSGI 2.0.17.1 (64bit) on [Wed Dec 12 22:54:04 2018] ***
compiled with version: 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.11.45.5) on 11 December 2018 15:35:49
os: Darwin-18.2.0 Darwin Kernel Version 18.2.0: Fri Oct  5 19:41:49 PDT 2018; root:xnu-4903.221.2~2/RELEASE_X86_64
nodename: greenfrogui-MacBook-Pro.local
machine: x86_64
clock source: unix
pcre jit disabled
detected number of CPU cores: 8
current working directory: /Users/greenfrog/develop/TIL_Python/wsgi
detected binary path: /Users/greenfrog/.virtualenvs/django/bin/uwsgi
*** WARNING: you are running uWSGI without its master process manager ***
your processes number limit is 1418
your memory page size is 4096 bytes
detected max file descriptor number: 7168
lock engine: OSX spinlocks
thunder lock: disabled (you can enable it with --thunder-lock)
uWSGI http bound on :7777 fd 4
spawned uWSGI http 1 (pid: 5681)
uwsgi socket 0 bound to TCP address 127.0.0.1:49925 (port auto-assigned) fd 3
Python version: 3.7.0 (default, Oct 24 2018, 22:58:41)  [Clang 10.0.0 (clang-1000.10.44.2)]
*** Python threads support is disabled. You can enable it with --enable-threads ***
Python main interpreter initialized at 0x7fe123404860
your server socket listen backlog is limited to 100 connections
your mercy for graceful operations on workers is 60 seconds
mapped 72888 bytes (71 KB) for 1 cores
*** Operational MODE: single process ***
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x7fe123404860 pid: 5680 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI worker 1 (and the only) (pid: 5680, cores: 1)
```

이제 `curl`을 이용해서 요청을 넣어보자.  

```sh
$ curl -X GET http://localhost:7777
Hello World
```

`uWSGI`의 출력은 다음과 같다. 

```sh
[pid: 5680|app: 0|req: 1/1] 127.0.0.1 () {28 vars in 310 bytes} [Wed Dec 12 22:55:37 2018] GET / => generated 11 bytes in 0 msecs (HTTP/1.1 200) 1 headers in 44 bytes (2 switches on core 0)
```

앞서 설명한 내용들은 다음과 같은 콤포넌트들로 구성된것이다.  

>Client <-> uWSGi <-> Python Application

## Test your Django project

이번에는 앞서 파이썬 어플리케이션으로 사용한 `test.py` 대신에 `Django Application`을 이용해보자.   

우선 `Django Application`에는 다음 url을 제공하고 있다.  

>/hello/say/

다음 명령을 통해 `uWSGI`와 `Django Application`이 연결 된 서버를 실행하자. 이때 반드시 **Django의 manage.py가 존재하는 경로에서 다음 명령을 실행해야한다.**

>$ uwsgi --http :7777 --moudle django_server.wsgi

위 명령에서 사용된 옵션은 다음과 같다. 

* module django_server.wsgi : wsgi모듈을 지정한다.  

`uWSGI`와 `Django Application`이 실행 된 모습은 앞서 `test.py`를 사용할 때와 동일하다. 이제 다음 명령을 통해 `Django Application`으로 요청을 전달해보자.  

```sh
$ curl -X GET http://localhost:7777/hello/say/
{"res": "Hello"}
```

앞서 설명한 내용들은 다음과 같은 콤포넌트드로 구성된것이다.  

>Client <-> uWSGi <-> Django Application

## Basic NginX

여기서는 간단히 NginX에 대해서 알아보자. 

### Start NginX with Docker

도커를 이용해서 `NginX`를 이미지를 `DockerHub`를 통해 내려받자.  

>$ docker pull nginx

```sh
$ docker pull nginx
Using default tag: latest
latest: Pulling from library/nginx
a5a6f2f73cd8: Pull complete
1ba02017c4b2: Pull complete
33b176c904de: Pull complete
Digest: sha256:5d32f60db294b5deb55d078cd4feb410ad88e6fe77500c87d3970eca97f54dba
Status: Downloaded newer image for nginx:latest
$
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
nginx               latest              568c4670fa80        2 weeks ago         109MB
```

이제 다음 명령을 통해 `NginX` 컨테이너를 올려보자. 

>$ docker run --name study-nginx -p 8080:80 -d nginx

위 명령을 통해 `NginX` 컨테이너를 올린 후 Browser를 통해 `localhost:8080`에 접근하면 `Welcome to nginx!`페이지가 출력된다.  






# Reference 

* [Setting up Django and your web server with uWSGI and nginx](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)