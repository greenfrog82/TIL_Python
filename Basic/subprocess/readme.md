# [subprocess](https://docs.python.org/2/library/subprocess.html#module-subprocess)

`Python 3.7`

`subprocess` 모듈은 새로운 프로세스를 생성, 생성 된 프로세스의 in/out/error 파이프 연결 그리고 생성 된 프로세스의 리턴값을 얻어올 수 있도록 한다. 이 모듈은 다음과 같이 오래된 모듈과 함수들을 대체할 목적을 가지고 있다. 

```python
os.system
os.spawn*
```

여기서는 `subprocess`를 사용하는 방법에 대해서 알아보도록 하자.  

## Using subprocess module

일반적인 경우에 서브 프로세스를 생성하기 위해 권장되는 방식은 `run()`함수를 사용하는 것이다. 서브 프로세스를 좀 더 고수준으로 다루고자 한다면 `Popen`인터페이스를 직접 사용할 수 있다.  

`run()`함수는 Python3.5에서 추가되었는데, 이전 버전과의 호환을 위해 `Older high-level API`를 따로 제공하고 있다.   

### subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)

`args` 파라메터에 의해 전달 된 명령을 실행하고 완료될 때 까지 기다렸다가 `CompletedProcess`인스턴스를 반환한다. 

#### Example

`run()`를 통해서 파이썬의 [Click](https://click.palletsprojects.com/en/7.x/)패키지를 설치해보자. 예제코드는 다음과 같다.

[run_using_pip.py](./run_using_pip.py)
```python
from subprocess import run

cp = subprocess.run(['pip', 'install', 'Click'])
print(cp)
```

출력결과를 보면 `capture_output`옵션을 별도로 주지 않았기 때문에 기본값이 `False`로 설정되어있으므로 `stdout`을 화면에 출력하고있는 것을 알 수 있다.  

```sh
Collecting Click
  Downloading https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl (81kB)
    100% |████████████████████████████████| 81kB 1.1MB/s
Installing collected packages: Click
Successfully installed Click-7.0
```

### class subprocess.CompletedProcess

`run()`가 리턴하는 인스턴스의 클래스로 완료된 프로세스의 정보를 담고있다. 

#### args

완료된 프로세스를 생성하는데 사용되었던 파라메터이다. 이 값은 `list`이거나 `string`이다. 

#### returncode

완료된 프로세스의 상태를 나타내는 종료 코드이다. 일반적으로 프로세스가 정상적으로 완료되면 **0**을 반환한다.  
`POSIX`에서 프로세스가 강제 종료되면 음수값을 반환한다. 

#### stdout

완료된 프로세스로부터 캡쳐된 `stdout`이다. `run()`함수가 `encoding`, `errors` 또는 `text=True`일 때, byte 시퀀스나 문자열 형태로 캡쳐된다. 만약 앞서 나열한 파라메터가 `None`인 경우 캡쳐되지 않는다. 

만약, 서브 프로세스가 `strerr=subprocess.STDOUT`설정으로 실행된 경우, `stdout`과 `stderr`는 하나로 묶이게 되고 `stderr`는 `None`을 반환한다. 

#### stderr

완료된 프로세스로부터 캡쳐된 `stderr`이다.  `run()`함수가 `encoding`, `errors` 또는 `text=True`일 때, byte 시퀀스나 문자열 형태로 캡쳐된다. 만약 앞서 나열한 파라메터가 `None`인 경우 캡쳐되지 않는다. 

#### check_returncode()

만약 `returncode`가 0이 아니면, `CalledProcessError`를 발생시킨다. 