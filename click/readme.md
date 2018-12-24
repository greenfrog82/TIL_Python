# [Click](https://click.palletsprojects.com/en/7.x/)

`Click`은 적은 코드로 멋진 명령행 인터페이스를 개발하기 위한 파이썬 패키지이다. `Click`은 매우 높은 수준으로 설정이 가능하지만, 기본 설정만으로도 충분히 사용할 수 있다.  

`Click`은 명령행 툴을 빠르고 쉽게 개발하기 위한 목적으로 개발되었고 다음 세가지 특징을 가지고 있다.  

* 임의의 중첩 된 명령
* 자동 `help` 페이지 생성
* 런타임에 subcommands의 lazy 로딩 지원

여기서는 위와 같은 특징을 갖은 `Click`이 사용법을 기초 차근차근 알아보도록 하자.  

## How to install Click

`Click`은 다음과 같이 설치가 가능하며, `virtualenv`환경 안에서 설치할 것을 권장한다.  

>$ pip install click

## Simple Example

다음은 `Click` 공식문서의 기본 예제이다. 이를 통해 `Click`의 간단한 사용 예를 확인해보자.  

[Example](./hello.py)
```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    for x in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

이제 위 코드를 실행시켜보자. `Your name`이라는 프롬프트가 실행되고 이름을 입력하면 `--count`옵션으로 전달 된 횟수만큼 이름이 반복 출력된다. 

```sh
$ python hello.py --count=3
Your name: greenfrog
Hello greenfrog!
Hello greenfrog!
Hello greenfrog!
```

`--help` 옵션을 통해 자동으로 생성 된 `help page`도 확인 할 수 있다.  

```sh
$ python hello.py --help
Usage: hello.py [OPTIONS]

Options:
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
```

