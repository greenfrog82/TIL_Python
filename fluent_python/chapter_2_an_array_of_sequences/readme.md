# Chapter 2. An Array of Sequences

## Overview of Built-In Sequences

표준 라이브러리는 C로 구현 된 다양한 sequence type을 제공한다.

### Container sequences

list, tuple 그리고 collections.deque와 같은 Container sequences는 다른 타입의 아이템들을 저장할 수 있다. 

### Flat sequences

str, bytes, bytearray, memoryview 그리고 array.array와 같은 Flat sequences는 동일한 타입의 아이템들만 저장할 수 있다. 

### Mutable sequences

list, bytearray, array.array, collection.deque 그리고 memoryview는 이를 구성하고 있는 아이템을 변경할 수 있는 sequence이다. 

### Immutable sequnces

tuple, str 그리고 bytes는 이를 구성하고 있는 아이템을 변경할 수 없는 sequence이다. 

## List Comprehensions and Generator Expressions

`list comprehension`(for `list`) 또는 `generator expression`(`list`를 제외한 모든 sequence)는 sequence를 생성하기 위한 빠른 방법이다.  
이것은 좀 더 가독성이 높으며 때때로 좀 더 빠르다.   

### SYNTAX TIP

파이썬 코드에서는 [], {} 또는 () 안에서 `line break`가 무시된다. 따라서 listcomp, generator expression, dictionarycomp, setcomp에서는 `\`을 사용하지 않아도 된다.  
다음과 같이 ~

```python
>>> [(i, j) for i in range(3)
...         for j in range(3)]
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
>>> ((i, j) for i in range(3)
...         for j in range(3))
<generator object <genexpr> at 0x10b398b10>
```

### LISTCOMPS NO LONGER LEAK THEIR VARIABLES

`Python 2.x`에서 `listcomp`을 사용할 때 `listcomp`의 scope안에 있는 변수명과 밖에있는 변수명이 동일할 경우 scope 밖에있는 변수의 값이 `listcomp`에 의해 변경되는 문제가 있었다.  

```python
Python 2.7.10 (default, Aug 17 2018, 17:41:52)
Type "copyright", "credits" or "license" for more information.

IPython 5.8.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: x = 'test'

In [2]: [x for x in range(10)]
Out[2]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [3]: x
Out[3]: 9
```

하지만, `Python 3.x`에서 `listcomp`, `generator`, `setcomp` 그리고 `diccomp`의 경우 자신의 **local scope**를 가지고 있기 때문에 이와같은 문제가 발생하지 않는다.  

```python
Python 3.7.0 (default, Oct 12 2018, 10:00:43)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.0.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: x = 'test'

In [2]: [x for x in range(10)]
Out[2]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [3]: x
Out[3]: 'test'
```

`Python 2.x`와 `Python 3.x`에서 `generator`, `setcomp` 그리고 `diccomp` 각각 앞서 설명한대로 동작하는지 확인해보자.  

#### Python 2.7.10

앞서 `Python 2.7.10`에서 `listcomp`를 사용할 때, `listcomp` 바깥 scope 변수의 값을 `listcomp`에서 변경하는것을 확인하였다. 하지만, `generator`, `setcomp` 그리고 `diccomp`에서는 전혀 다르게 동작하는 것을 확인할 수 있다. 앞서 `Python 3.x`에서 설명했던 `generator`, `setcomp` 그리고 `diccomp`와 동일하게 동작함을 알 수 있다. 

```python
In [25]: list(x for x in xrange(10))
Out[25]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [26]: x
Out[26]: 'test'

In [27]: x = 'test'

In [28]: {x for x in xrange(10)}
Out[28]: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

In [29]: x
Out[29]: 'tet'

In [32]: {x:'value' for x in xrange(10)}
Out[32]:
{0: 'value',
 1: 'value',
 2: 'value',
 3: 'value',
 4: 'value',
 5: 'value',
 6: 'value',
 7: 'value',
 8: 'value',
 9: 'value'}

In [33]: x
Out[33]: 'test'
```

#### Python 3.7.0

앞서 `Python 2.7.10`에서와 완전히 동일한 결과를 보여준다. 

```python
In [1]: x = 'test'

In [2]: list(x for x in range(10))
Out[2]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

In [3]: x
Out[3]: 'test'

In [4]: {x for x in range(10)}
Out[4]: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

In [5]: x
Out[5]: 'test'

In [6]: {x:'value' for x in range(10)}
Out[6]:
{0: 'value',
 1: 'value',
 2: 'value',
 3: 'value',
 4: 'value',
 5: 'value',
 6: 'value',
 7: 'value',
 8: 'value',
 9: 'value'}

In [7]: x
Out[7]: 'test'
```

마지막으로, `for loop`의 경우는 어떻게 동작할까? 이 경우는 Python의 버전과는 무관하며 지역변수이기 때문에 `for loop`에서 사용하는 변수와 동일한 변수명이 존재한다면 해당 변수의 값이 `for loop`에 의해 변경된다.

다음 예제를 보면 `Python 2.x`와 `Python 3.x`가 동일한 결과를 출력하고 있음을 알 수 있다.

```python
# Python 2.7.10
In [4]: x = 'test'

In [5]: for x in range(10):
   ...:     x
   ...:

In [6]: x
Out[6]: 9

# Python 3.7.0
In [5]: x = 'test'

In [6]: for x in range(10):
   ...:     x

In [7]: x
Out[7]: 9
```

## Slicing

list, tuple, str 그리고 모든 sequence 타입의 공통 기능은 `slicing` operation을 제공한다는 것이다. 이것은 일반적으로 파이썬 개발자들이 알고있는것 보다 더 강력하다.   

### Why Slices and Range Exclude the Last Item

`slice`와 `range`에서 마지막 아이템을 제외하는 파이써닉 규칙은 제로 베이스 인덱싱을 사용하는 언어들과 같이 잘 동작한다 이러한 규칙은 몇가지 편리한 기능을 제공한다. 

* `stop` 포지션의 값을 보면, `slice`또는 `range`의 길이를 알 수 있다. 
    ```python
    >>> arr = list(range(5))
    >>> arr
    [0, 1, 2, 3, 4]
    >>> arr[:3]
    [0, 1, 2]
    ```
* `start`와 `stop` 포지션이 주어졌을 때 **stop-start**를 통해 길이를 구할 수 있다.
    ```python
    >>> arr[2:5]
    [2, 3, 4] 
    ```
* 인덱스 값 하나를 통해서 sequence를 이등분 할 수 있다. 
    ```python
    >>> arr[:3]
    [0, 1, 2]
    >>> arr[3:]
    [3, 4]
    ```

### Slice Objects

`[start:stop:step]`의 `step`을 통해 sequence를 띄엄띄엄 접근하거나 음수를 전달해서 거꾸로 데이터에 접근할 수 있다.   

```python
>>> s = 'bicycle'
>>> s[::3]
'bye'
>>> s[::-1]
'elcycib'
>>> s[::-2]
'eccb'
```

`start:stop:step`은 반드시 `[]`만 유효하다. `slice(start, stop, step)`을 통해 `slice`객체를 생성할 수 있다. 사실, sequence arr가 있다고 가정하고 arr[start:stop:step]이라고 코딩을 할 경우 파이썬은 해당 코드를 다음과 같이 해석한다. 

```python
arr = [1, 2, 3, 4, 5]
arr[1:3:2]
# 파이썬은 다음과 같이 코드를 해석
arr.__getitem__(slice(1, 3, 2))
```

다음 코드는 invoice라는 텍스트를 파싱하는데 있어서, 앞서 설명했던 `slice`의 특징을 이용하고 있다. `slice`를 for-loop안에 하드코딩하지 않고, 미리 `slice`객체를 생성한 후 가독성 있는 변수에 할당하여 각각 어떤 데이터를 파싱하고 있는지 알기 쉽게 하였다.  

```python
>>> invoice = """
... ... 0.....6.................................40........52...55........
... ... 1909  Pimoroni PiBrella                     $17.50    3    $52.50
... ... 1489  6mm Tactile Switch x20                 $4.95    2     $9.90
... ... 1510  Panavise Jr. - PV-201                 $28.00    1    $28.00
... ... 1601  PiTFT Mini Kit 320x240                $34.95    1    $34.95
... ... """

>>> UNIT_PRICE = slice(40, 52)

>>> DESCRIPTION = slice(6, 40)

>>> line_items = invoice.split('\n')[2:]

>>> for item in line_items:
...     print(item[UNIT_PRICE], item[DESCRIPTION])
        $17. 09  Pimoroni PiBrella
         $4. 89  6mm Tactile Switch x20
        $28. 10  Panavise Jr. - PV-201
        $34. 01  PiTFT Mini Kit 320x240
```

### Multidimensional Slicing and Ellipsis

`NumPy`라이브러리를 사용하면 다차원에 대한 `slicing`을 사용할 수 있다. 이 경우 `index`와 `slicing`을 `Tuple`로 전달할 수 있다. 하지만, Pyhton Buil-in의 sequence들은 1차원이다. 따라서 하나의 `index`또는 `slicing`만 사용가능하다. 

`Ellipsis`는 Numpy에서 사용되는건데 정확히 뭔지 모르겠다 ;; 

### Assigning to Slices

`Mutable sequence`들은 `slice`표현과 `assignment` 그리고 `del`을 통해 새로운 sequence를 생성하지 않고 접목, 잘라내기 등과 같이 sequence를 변경할 수 있다.

다음 예제를 보자. `slice`와 함께 `assignment`와 `del`을 통해 `Mutable sequence`를 수정하고 있다. 

먼저 아래 코드를 보면 2, 3, 4번 인덱스의 데이터를 수정하도록 설정해두고 실제로는 원소가 2개인 튜플만 전달하고 있다. 이 경우 결과를 보면 2, 3번째 인덱스의 값이 각각 원소의 값으로 치환되고 **4번째 인덱스의 값이 삭제**된것을 알 수 있다. 

```python
>>> l = list(range(10))
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> l[2:5] = [20, 30]
>>> l
[0, 1, 20, 30, 5, 6, 7, 8, 9] 
```

`del`명령을 통해 5, 6번 인덱스의 데이터를 삭제해보자.   
다음 예제를 보면 5, 6번 인덱스에 대응하는 값인 6과 7이 삭제된것을 확인할 수 있다. 

```python
>>> del l[5:7]
>>> l
[0, 1, 20, 30, 5, 8, 9]
```

이번에는 3번 인덱스부터 2칸씩 이동하면서 데이터를 치환해보자.   
3번과 5번에 인덱스에서 대응하는 값이 각각 11, 22로 치환된것을 확인할 수 있다.

```python
>>> l[3::2] = [11, 22]
>>> l
[0, 1, 20, 11, 5, 22, 9] 
```

앞선 예제를 보면 값이 할당할 때 `sequence`를 전달하고 있는데, `scala`를 전달하면 어떻게 될까?  
다음과 같이 `TypeError: can only assign an iterable`을 출력한다. 

```pyhon
>>> l[2:5] = 100
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only assign an iterable

can only assign an iterable
```

따라서 **하나의 값만 전달한다고 하더라도 반드시 iterable 객체**를 전달해야한다.   
다음과 같이 리스트를 전달하면 정상적으로 동작한다. 

```python
>>> l[2:5] = [100]
>>> l
[0, 1, 100, 22, 9]
```

지금까지는 리스트 범위를 넘지 않는 리스트만을 전달하였지만, 이번에는 `slice`된 리스트의 범위를 벗어나는 데이터를 전달해보자.  
다음과 같이 8, 9 인덱스에 대응하는 값에 100, 200, 300, 400값이 들어있는 배열을 전달해보자.  
예상해보면 100, 200 원소들만 전달될것 같지만 그렇지 않다. 결과를 확인해보자.

```python
>>> l = list(range(10))
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l[8:10] = [100, 200, 300, 400]
>>> l
[0, 1, 2, 3, 4, 5, 6, 7, 100, 200, 300, 400]
```

## Using + and * with Sequences

파이썬은 **모든 타입의 sequence**에 대해서 `+`와 `*` 연산을 제공한다. 해당 연산자들은 늘 새로운 sequence를 생성하며 피연산자를 변경하지 않는다.    

### +

일단적으로 `+`연산자는 반드시 **동일한 타입의 sequence**에 대해서 두 sequence를 연결하여 새로운 sequene를 만들어낸다.  

다음 예제를 보면 두 list를 `+`연산을 통해 연결하고 있다.  

```python
>>> a = list(range(5))
>>> b = list(range(5,10))
>>> a
[0, 1, 2, 3, 4]
>>> b
[5, 6, 7, 8, 9]
>>> a + b
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> a
[0, 1, 2, 3, 4]
>>> b
[5, 6, 7, 8, 9]
>>>
```

앞서 `+`연산은 **동일한 타입의 sequence**를 연결해준다고 했다. 그럼 **다른 타입의 sequence**를 연결해보면 어떻게 될까?  
다음과 같이 에러가 `TypeError`가 발생한다. 

```python
>>> a = list(range(5))
>>> b = tuple(range(5,10))
>>> a
[0, 1, 2, 3, 4]
>>> b
(5, 6, 7, 8, 9)
>>> a + b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate list (not "tuple") to list

can only concatenate list (not "tuple") to list
```

반대로 연결을 시도해보아도 마찬가지 결과가 출력된다.  

```python
>>> b + a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate tuple (not "list") to tuple

can only concatenate tuple (not "list") to tuple
```

### *

`*`연산자는 sequence의 원소를 n번 반복하는 새로운 sequence를 생성한다.  
다음 예제를 확인하자.  

```python
>>> l = list(range(1, 4))
>>> l
[1, 2, 3]
>>> l = tuple(range(1, 4))
>>> l * 3
(1, 2, 3, 1, 2, 3, 1, 2, 3)
>>> 5 * 'abcdef'
'abcdefabcdefabcdefabcdefabcdef'
```

### Building Lists of Lists

여기서는 `*`연산자로 `list of lists`를 초기화할 때 발생할 수 있는 문제에 대해서 다룬다. 

다음 예제를 보자. `listcomp`와 `*`연산자를 통해 각각 언더바 3개 원소를 갖는 리스트를 3개 갖는 리스트를 생성했다. 리스트를 생성한 후 1번째 리스트의 2번째 인덱스의 값을 'X'으로 바꾸고 있다.   
결과를 보면 기대한대로 잘 동작하고 있다.  

```python
>>> board = [['_']  * 3 for i in range(3)]
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[1][2] = 'X'
>>> board
[['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]
```

그런데 `listcomp`를 사용하지 않고 [['_'] * 3]를 3번 곱해서 똑같은 결과를 만들 수 있을것 같다. 정말 그럴까?  
다음 예제를 보자. 일단 생성 된 결과를 보면 의도한대로 잘 동작하는것 같다. 

```python
>>> board = [['_'] * 3] * 3
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
```

이번에는 `listcomp`로 생성했던 예제와 동일하게 board[1][2]에 'X'를 대입해보자.   

```python
>>> board[1][2] = 'X'
>>> board
[['_', '_', 'X'], ['_', '_', 'X'], ['_', '_', 'X']]
```

의도치 않은 결과가 출력되었다. 왜 그럴까?  
다음 예제를 보면 원인을 알 수 있다. 앞서 예제는 다음 예제와 같이 리스트를 생성해두고 같은 레퍼런스를 리스트에 추가한것과 같기 때문에 문제가 발생한것이다.   

```python
>>> row = ['_'] * 3
>>> board = []
>>> for i in range(3):
...     board.append(row)
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[1][2] = 'X'
>>> board
[['_', '_', 'X'], ['_', '_', 'X'], ['_', '_', 'X']]
```

반면에 정상적으로 동작했던 `listcomp`예제는 다음 코드와 같다.  

```python
>>> board = []
>>> for i in range(3):
...     row = ['_'] * 3
...     board.append(row)
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> board[2][1] = 'X'
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', 'X', '_']]
```

