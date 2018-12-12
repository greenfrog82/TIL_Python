# Setting up TFJ-API with uWSGI and NginX


본 문서는 TFJ-API에 uWSGI와 NginX를 연동하는 방법에 대해서 설명한다.  

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

# Reference 

* [Setting up Django and your web server with uWSGI and nginx](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)