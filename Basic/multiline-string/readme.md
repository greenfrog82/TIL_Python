# How to write multi-line string

파이썬에서 multi-line string을 사용하는 방법에 대해서 알아보자. 

## Using Triple quotes

`"""` 또는 `'''`으로 문자열을 감싸서 multi-line string을 표현할 수 있다.   

아래 예제를 보면 `"""`통해 multi-line string을 표현하고 있다.

[ex_triple_quotes.py](./ex_triple_quotes.py)

```python
def get_msg():
    return """
    --- Test ---
    greenfrog
    ------------
    """

print(get_msg())
```

그런데 위 예제의 실행결과를 보면 아래와 같이 **코드에서의 들여쓰기가 포함되어 출력**되어버린다. 

```sh
$ python ex_triple_quotes.py

    --- Test ---
    greenfrog
    ------------
```

때문에 `"""`을 통해 multi-line string을 표현할 때는 `textwrap`모듈의 `dedent`함수를 함께 사용해야한다. 

[ex_triple_quotes.py](./ex_triple_quotes.py)

```python
from textwrap import dedent


def get_msg():
    return """
    --- Test ---
    greenfrog
    ------------
    """

print(dedent(get_msg()))
```

이제 출력결과를 보면 **코드에서의 들여쓰기가 지워진 상태로 출력**되는것을 알 수 있다. 

```sh
$ python ex_triple_quotes.py

--- Test ---
greenfrog
------------
```

## Using the parentheses 

앞서 `"""`를 사용하는 경우는 의도와 달리 들여쓰기가 포함되는것을 알 수 있었다. 때문에 이를 정리하기 위해서 `textwrap.dedent()`함수를 사용했어야한다.  
이번 방법은 괄호를 사용하는 것인데 `"""`보다 더 간편한것 같다. 다음 에제와 실행결과를 보자.

```python
def get_msg():
    return (
        "--- Test ---\n"
        "greenfrog\n"
        "------------\n"
    )

print(get_msg())
```

```sh
$ python ex_parentheses.py
--- Test ---
greenfrog
------------
```

# Reference

* [Python Idioms: Multiline Strings](https://amir.rachum.com/blog/2018/06/23/python-multiline-idioms/)
* [Pythonic way to create a long multi-line string](https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string)