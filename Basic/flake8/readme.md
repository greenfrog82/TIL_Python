# flake8

## How to check trailling comma

다음 예제를 `flake8`을 통해 검사해보자. 

```python
# ex.py
import httplib

class Test:
    pass



repo = {
    'name': 'greenfrog'
}


```

```sh
$ flake8 ex.py
ex.py:1:1: F401 'httplib' imported but unused
ex.py:3:1: E302 expected 2 blank lines, found 1
ex.py:8:1: E303 too many blank lines (3)
```

일반적으로 `flake8`은 `trailling comma`를 검사하지 못한다.   
[PEP 8 -- Style Guide for Python Code, When to Use Trailing Commas
](https://www.python.org/dev/peps/pep-0008/#when-to-use-trailing-commas)을 읽어보면 `trailling comma`는 선택사항이기 때문인것 같다.  

만약 `flake8`을 통해 `trailling comma`를 검사하고자 한다면, [flake8-commas](https://pypi.org/project/flake8-commas/)이라는 라이브러리를 사용해보자. 설치는 다음 명령을 통해 할 수 있다.  

>pip install flake8-commas

설치가 됐으면 바로 사용할 수 있다. 

```sh
$ flake8 ex.py
./ex.py:1:1: F401 'httplib' imported but unused
./ex.py:3:1: E302 expected 2 blank lines, found 1
./ex.py:8:1: E303 too many blank lines (3)
./ex.py:9:24: C812 missing trailing comma
```

# Reference

* [How to Use Flake8](https://simpleisbetterthancomplex.com/packages/2016/08/05/flake8.html)
* [flake8-commas](https://pypi.org/project/flake8-commas/)