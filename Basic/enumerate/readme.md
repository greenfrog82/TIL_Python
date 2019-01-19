# [Enum](https://docs.python.org/3/library/enum.html)

파이썬에서 enumeration을 정의할 수 있는 방법을 제공한다. Enum을 상속하는 클래스의 정의들은 구별이 가능하고 iterate가 가능하다. 

## Module Contents 

`Enum`모듈은 4가지(Enum, IntEnum, Flag, IntFalg) 종류의 enumeration 클래스를 정의할 수 있다. 그리고 `unique()` 데코레이터와 `auto` 헬퍼 함수를 제공한다. 

* **class enum.Enum** : 기본 enumeration
* **class enum.IntEnum** : int, Enum의 mixin 클래스
* **class enum.IntFlag** : int, Flag의 mixin 클래스
* **class enum.Flag** : ??
* **enum.unique()** : 하나의 열거 이름이 값과 하나의 값과 맵핑되는것을 보장해주는 데코레이터
* **class enum.auto** : 해당 클래스의 인스턴스는 열거 이름에 대해서 적절한 값으로 치환된다. 

New in version 3.6: Flag, IntFlag, auto

## Creating an Enum

`Enumeration`은 `class` 타입이나 `Function API`를 통해 정의할 수 있다. 일단 `class`타입으로 정의하는 방법은 다음과 같다.  
정의한 `Enumeration` 이름과 값의 비교는 허용되지 않으면, 이를 하기위해서는 `value` property를 사용해야한다.  

```python
>>> from enum import Enum
...
>>> class Color(Enum):
...     RED = 1
...     GREEN = 2
...     BLUE = 3
>>>
>>> Color.RED == 1
False
>>> Color.RED.value == 1
True
```

다음과 같이 여러 타입의 값을 사용할 수 도 있다. 

```python
>>> class Color(Enum):
...     RED = '1'
...     GREEN = 1.2
...     BLUE = 1
>>>
>>> Color.RED
<Color.RED: '1'>
>>> Color.GREEN
<Color.GREEN: 1.2>
>>> Color.BLUE
<Color.BLUE: 1>
>>> Color.RED == 1
False
>>> Color.RED == '1'
False
>>> Color.RED.value == '1'
True
>>> Color.RED.name
'RED'
```

`Enumerator`에 정의한 멤버는 상수이기 때문에 값을 할당할 수 없다. 만약 할당을 시도한다면 `AttributeError`가 발생한다. 

```python
>>> Color.RED = 100
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/enum.py", line 383, in __setattr__
    raise AttributeError('Cannot reassign members.')
AttributeError: Cannot reassign members.

Cannot reassign members.
```

`Enumerator`는 `iterate`도 지원을 하는데 멤버가 정의 된 순서를 따른다. 

```python
>>> class Color(Enum):
...     RED = 3
...     GREEN = 2
...     BLUE = 1

>>>
>>> for color in Color:
...     print(color)
Color.RED
Color.GREEN
Color.BLUE

>>> [color for color in Color]
[<Color.RED: 3>, <Color.GREEN: 2>, <Color.BLUE: 1>]
```

## Derived Enumerations

### IntEnum

`IntEnum`은 `integer`와 `IntEnum`을 통해 정의된 다른 타입끼리 비교가 가능하다.

```python
>>> from enum import IntEnum
...
...
... class Shape(IntEnum):
...     CIRCLE = 1
...     SQUARE = 2
...
... class Request(IntEnum):
...     POST = 1
...     GET = 2

>>> Shape.CIRCLE == 1
True

>>> Shape.CIRCLE == 2
False

>>> Shape.CIRCLE == Request.POST
True

>>> Shape.CIRCLE == Request.GET
False
```
