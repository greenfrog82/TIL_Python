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

다음과 같이 여러 타입의 값을 사용할 수 있다. 

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

또한 정의되지 않은 멤버를 호출 할때 역시 `AttributeError`가 발생한다.   

```python
>>> Color.HEAD
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/enum.py", line 346, in __getattr__
    raise AttributeError(name) from None
AttributeError: HEAD

HEAD
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

`Enumeration`의 멤버는 hashable하기 때문에 dictionary나 set에서 사용될 수 있다. 

```python
>>> from enum import Enum

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2

>>> set_ = {Color.RED, Color.BLUE}
>>> set_
{<Color.RED: 1>, <Color.BLUE: 2>}

>>> 1 in set_
False
>>> Color.RED in set_
True
```

## Programmatic access to enumeration members and their attributes

`Enumeration`을 정의하기 전 사용되던 함수의 반환값을 통해 `Enumeration`에 정의 된 멤버에 접근하기 위해서는 동적으로 멤버를 얻어올 수 있는 방법을 사용해야한다. 

먼저 다음과 같은 `Enumeration` Color가 있다고 가정하자.   

```python
>>> class Color(Enum):
...     RED = 1
...     GREEN = 2
...     BLUE = 3
```

그리고 Color가 정의되기 전, 사용되던 함수에서 Color 멤버에 대응하는 값을 반환한다고 가정하자. 그러면 다음과 같이 1이라는 값이 반환되었을 때 Color의 RED 멤버에 접근하려면 어떻게 해야할까? 다음 코드를 참고하자.  

```python
>>> Color(1)
<Color.RED: 1>
```

만약 Color 멤버에 대응하는 값을 전달하지 않는다면, `ValueError`를 발생시킨다.   

```python
>>> Color(100)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/enum.py", line 307, in __call__
    return cls.__new__(cls, value)
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/enum.py", line 555, in __new__
    return cls._missing_(value)
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/enum.py", line 568, in _missing_
    raise ValueError("%r is not a valid %s" % (value, cls.__name__))
ValueError: 100 is not a valid Color

100 is not a valid Color
```

Color 멤버의 이름에 대응하는 값을 반환하는 함수가 있다고 가정하자. 이러한 경우는 어떻게 Color의 멤버에 접근할 수 있을까?

```python
>>> Color['RED']
<Color.RED: 1>
``

만약, Color 멤버에 대응하는 이름을 전달하지 않는다면, `KeyError`를 발생시킨다.   

```python
>>> Color['HOHO']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/enum.py", line 349, in __getitem__
    return cls._member_map_[name]
KeyError: 'HOHO'

'HOHO'
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
