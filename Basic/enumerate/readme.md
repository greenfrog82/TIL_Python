# Enum


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
