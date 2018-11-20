# Chapter 1. The Python Data Model

파이썬의 특징 중 하나는 일관성이다. 파이썬을 잠시만 사용해보면 새로운 기능에 대한 올바른 추측을 해볼 수 있다.  

파이썬을 사용할 때 우리가 일반적인 언어와 다르다고 생각하는 모든것들을 `파이썬 데이터 모델`이라고한다.  

`파이썬 데이터 모델`은 sequences, iterators, functions, classes, context manager 그리고 기타 등등 언어의 빌딩블록의 인터페이스를 형식화한다.   

파이썬 인터프리터는 종종 특별한 문법에 의해 실행되는 기본 오브젝트의 오퍼레이션을 실행하기 위해 `special method`를 호출한다. 이 특별한 메소드는 메소드명 앞뒤에 double under score를 붙인다(i.e. __getitem__). 예를들어, obj[key]문법은 __getitem__ 메소드를 통해서 제공된다. obj[key]를 동작시키기 위해서는 파이썬 인터프리터가 obj.__getitem__(key)를 호출한다. 

이러한 `special method`이름들은 다음과 같은 기본 언어구조를 여러분의 오브젝트가 구현, 제공하고 상호작용 할 수 있다록한다.  

* Iteration
* Collections
* Attribute access
* Operator overloding
* Function and method invocation
* Object creation and destruction
* String representation and formatting
* Managed contexts (i.e. with blocks)

>### MAGIC AND DUNDER
>magic method는 `special method`의 속어이다. 따라서 `special method`를 사용하거나 `dunder method`라고 부르도록 하자.

## A Pythonic Card Deck

`special method`의 강력함을 느껴보기 위해 간단한 에제를 하나 만들어보자.  
여기서 소개할 `special method`는 `__getitem__`과 `__len__`이다. 

```python
import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
```
```python
In [3]: beer_card = Card('7', 'diamonds')
In [4]: beer_card
Out[4]: Card(rank='7', suit='diamonds')
In [5]: deck = FrenchDeck()
In [6]: len(deck)
Out[6]: 52
In [9]: deck[0]
Out[9]: Card(rank='2', suit='spades')
In [10]: deck[1]
Out[10]: Card(rank='3', suit='spades')
In [16]: choice(deck)
Out[16]: Card(rank='9', suit='diamonds')
In [17]: choice(deck)
Out[17]: Card(rank='5', suit='spades')
In [18]: choice(deck)
Out[18]: Card(rank='8', suit='spades')
```

위 예제의 실행결과를 보면 `FrenchDesck`클래스가 `__getitem__`와 `__len__` `special method`를 구현함으로서 `len() method`와 `indexer`를 그대로 사용하고 있음을 알 수 있다.  
또한 `__getitem__`을 구현함에 따라 `indexer`를 통해 `Sequence`에서 랜덤으로 요소를 반환하는 `random.choice`함수도 사용할 수 있다.  
참고로 `__getitem__`을 구현하지 않았다면, `random.choice`함수를 호출할 때 다음과 같은 에러가 발생한다.   

```python
In [30]: choice(deck)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-30-c6ed376cb18f> in <module>
----> 1 choice(deck)

~/.pyenv/versions/3.7.0/lib/python3.7/random.py in choice(self, seq)
    260         except ValueError:
    261             raise IndexError('Cannot choose from an empty sequence') from None
--> 262         return seq[i]
    263
    264     def shuffle(self, x, random=None):

TypeError: 'FrenchDeck' object does not support indexing
```

위 예제를 통해 우리는 `Python Data Model`을 활용하기 위해 `special method`를 사용하는 두가지 이점을 알 수 있다.

* FrenchDeck 클래스를 사용하는 개발자가 표준 오퍼레이션을 위한 임의의 메소드 이름을 기억하지 않아도 된다. 예를들어 FrenchDeck 객체가 가지고 있는 카드의 개수를 구하기 위해 size 메소드를 호출해야하는지, length 메소드를 호출해야하는지 고민할 필요가 없다. 
* 파이썬의 방대한 표준 라이브러리를 쉽게 이용할 수 있다. 따라서 FrenchDeck 클래스의 카드를 랜덤으로 선택하기 위한 함수를 또 만들필요가 없다. DRY

더 좋은것은 `__getitem__`이 `[] operator`를 위임하고 있기 때문에 `slice`를 자동적으로 제공한다.  

```python
In [44]: deck[:3]
Out[44]:
[Card(rank='2', suit='spades'),
 Card(rank='3', suit='spades'),
 Card(rank='4', suit='spades')]

In [45]: deck[12::14]
Out[45]:
[Card(rank='A', suit='spades'),
 Card(rank='2', suit='clubs'),
 Card(rank='3', suit='hearts')]
```

`__getitem__`을 구현하였으므로 해당 오브젝트의 객체는 `iterable`이다. 따라서, 다음과 같이 사용할수도 있다.  

```python
In [54]: for card in deck:
    ...:     print(card)
Card(rank='2', suit='spades')
Card(rank='3', suit='spades')
...
In [55]: [card for card in deck]
Out[55]:
[Card(rank='2', suit='spades'),
 Card(rank='3', suit='spades'),
...
```

`reversed`도 역시 사용 가능하다. 

```python
In [57]: for card in reversed(deck):
    ...:     print(card)
Card(rank='A', suit='hearts')
Card(rank='K', suit='hearts')
```

`iteration`은 종종 암묵적이다. 만약 `__contains__` 메소드가 정의되어 있지 않다면, `in` operator는 **sequential scan**을 수행한다.  

```python
In [60]: Card('Q', 'hearts') in deck
Out[60]: True
```

정렬을 해보자. 일반적인 랭킹 카드 시스템은 내림차순으로 정렬된다. 스페이드가 가장 높고, 그 다음은 하트, 다이아몬드 마지막으로 클럽 순이다. 
다음은 같은 랭키의 카드들을 내림차순으로 정렬한다.  

```python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in deck:
    print(card)

Card(rank='2', suit='clubs')
Card(rank='2', suit='diamonds')
Card(rank='2', suit='hearts')
Card(rank='2', suit='spades')
Card(rank='3', suit='clubs')
Card(rank='3', suit='diamonds')
Card(rank='3', suit='hearts')
Card(rank='3', suit='spades')
...
Card(rank='A', suit='clubs')
Card(rank='A', suit='diamonds')
Card(rank='A', suit='hearts')
Card(rank='A', suit='spades')
```

FrenchDeck 클래스가 `object` 클래스를 상속하긴 했지만, 앞서의 기능이 상속되지 않는다. `object` 클래스를 보면 FrenchDeck 클래스에서 구현한 `special method`는 정의되어 있지도 않다. 결국 FrenDeck의 기능들은 `data model`과 구성을 통해서 생성된다.   
FrenchDeck는 `__len__`과 `__getitem__`을 구현 함으로써, 마치 파이썬의 표준 sequence처럼 동작하고, 파이썬 표준 라이브러리를 통한 `iteration`이나 `slicing`같은 기능을 사용할 수 있다. 

>### HOW ABOUT SHUFFLING?
지금까지 FrenchDeck의 구현으로는 카드를 섞을 수 없다. 왜냐하면 _cards 멤버 변수가 private이고 이를 변경할 수 있는 기능을 제공하지 않기 때문이다. 물론 파이썬은 언어적기능으로 private를 제공하고 있지 않기 때문에 해당 멤버 변수에 직접 접근해서 변경이 가능하지만 .. 이 경우는 암묵적인 약속을 위반하는이므로 논외로 하고 ..   
따라서, 카드를 섞는 기능을 넣고 싶으면 `__setitem__ special method`를 사용할 수 있다. 
>
>참고로 `__setitem__`은 객체에서 indexer를 통해 값을 할당할 수 있도록 한다.

## How Special Methods Are Used

`special method`를 사용할 때 여러분이 알아둬야하는 하나는, 이는 파이썬 인터프리터에 의해 호출되어야지 여러분이 직접 호출해서는 안된다는 것이다.  
예를들어 my_object라는 사용자 정의 클래스의 인스턴스가 있다고 할때, `my_object.__len__()`이라는 코드를 작성하지 말고 `len(my_object)`라고 코드를 작성하자. `len(my_object)`라고 코드를 작성했을 때 파이썬의 인터프리터는 여러분이 작성한 사용자 정의 클래스의 `__len__`을 호출한다.   

하지만 `list, str, bytearray` 그리고 기타 등등의 파이썬 built-in 타입의 경우 파이썬 인터프리터는 좀 더 빠른 방법을 사용한다. `CPython`의 `len()`은 이러한 built-in 타입을 사용하는 경우, 가변 사이즈 build-in 오브젝트를 표현하는 `PyVarObject` C 구조체의 `ob_size`필드의 값을 반환한다. 이 경우 `special method`를 호출하는것보다 훨씬 빠르다.   

대개, `special method`의 호출은 암묵적이다. 예를들어, `for in x:`표현식은 사실 `iter(x)`를 호출하고 이는 결국 가능하면 `x.__iter__()`를 호출한다. 

**CHECK** 
다음 내용에서 `metaprogramming` 관련된 내용 이해 안됨. 

보통, `special method`를 직접 호출하는 경우는 가급적 없어야한다. `metaprogramming`을 많이 하지 않는 한, 명시적으로 호출하는 것보다 더 많이 `special method`를 구현해야한다.  
사용자의 코드에서 빈번하게 직접호출되는 유일한 `special method`는 `__init__`이다. 이 메소드는 사용자 정의 클래스의 `__init__` 메소드의 구현부에서 부모 클래스의 `__init__`을 호출할 때 명시적으로 호출된다.  

**CHECK**
앞서 `special method`를 사용하면, 이에 상응하는 built-in 함수를 호출하는것이 좋다고 했는데 built-in 타입을 사용할 때는 PyVarObject의 ob_size 와 같은 필드값을 사용하니 빠르다는건 알겠는데 `special method`는 결국 메소드를 호출해야하는데 다시 built-in 함수를 통해 호출해서 쓰라는 이야가 뭐지? 일관성때문에? 성능의 손해를 봐가면서?

만약 `special method`를 호출해야한다면, 일반적으로 `special method`를 호출해주는 `built-in function`을 사용하는것이 좋다. 이러한 `built-in function`들은 이에 상응하는 `special method`를 호출할 뿐만아니라, 서비스들도 제공하고 built-in type의 경우 `special method`를 콜하는 것보다 빠르다.  

`__foo__`와 같은 임의의 `special method`를 작성하지 말자. 지금은 사용되지 않을지 몰라도 새로운 버전에서 특별한 의미로 사용 될수도 있다. 

## Emulating Numeric Types

몇몇 `special method`들은 사칙연산을 수행할 수 있도록 한다.  
다음 예제를 참고하자. 

```python
from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        # return 'Vector(%r, %r)' % (self.x, self.y)
        return 'Vector({!r}, {!r})'.format(self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(2, 4) 
v2 = Vector(2, 1)
print(v1+v2) # Vector(4, 5)

v = Vector(3,4)
print(abs(v)) # 5.0

print(v * 3) # Vector(9, 12)
print(abs(v * 3)) # 15.0
```

## String Representation

`__repr__`은 object 검사를 위해 오브젝트를 표현하는 문자열을 얻기 위해 사용되며, `repr` build-in function에 의해서 호출된다. 만약 `__repr__`을 구현하지 않으면, 앞서 작성했던 Vector 클래스의 인스턴스는 `<Vector object at -x10e100070>`과 같은 문자열을 출력할 것이다.  

`interactive console`과 `debugger`는 실행된 표현식의 결과와 포맷을 출력하는 고전적인 방식으로 `%r` placeholder나, `string.format` 메소드의 `{!r}` conversion field를 사용하는 경우 `repr`을 호출한다. 

`__repr__`의 구현에서는 `%d`나 `%f`를 사용할 수 있음에도 불고하고 `%r`을 사용한것은 좋은 선택이다. 이는 `Vector(1, 2)`와 `Vector('1', '2')`는 객체를 생성하는데 있어서 아주 중요한 차이점(Vector는 numeric 타입의파라메터를 통해 생성된다.)을 가지고 있기 때문이다. 무슨 말인고 하니, **`__repr__`의 구현은 해당 인스턴스를 다시 생성하기 위해 필요한 정보들이 분명히 나타나야한다.**  
앞서 작성한 예제는 Vector 클래스 생성자의 파라메터가 numeric 타입이라 크게 관계가 없지만, 만약 오브젝트였다면 해당 오브젝트에 대한 상세가 출력되지 않을 것이다. 그러면 당연히 해당 출력을 통해 동일한 객체를 생성할 수 없다.  

`__str__`은 `str()`생성자와 `print` 함수에서 암시적으로 호출된다. `__repr__`이 개발자를 위한 정보를 전달한다면, `__str__`은 end user를 위한 정보를 전달하도록 구현되어야한다.

만약, `__repr__`과 `__str__` 중에 오직 하나의 메소드만 구현한다면, `__repr__`구현하자. `__str__`이 호출되야 하는 경우에 해당 메소드가 존재하지 않는다면 `__repr__`을 호출하기 때문이다. 

다음은 `__repr__`과 `__str__`을 `%s`와 `%r`을 통해 어떻게 호출되는지 확인하기 위한 에제이다.  
앞서 Vector 클래스에 다음과 같이 `__str__`메소드를 추가해보자. 

```python
def __str__(self):
    return '__str__'
```

그리고 다음 코드들을 실행해보자. 

```python
print('r : %r' % v) # r : Vector(3, 4)
print('s : %s' % v) # s : __str__
print('!r : {!r}'.format(v)) # !r : Vector(3, 4) 
print('!s : {!s}'.format(v)) # !s : __str__
```

다음은 앞서 정의한 `__str__`을 삭제하고 다시 테스트한 결과이다. `__repr__`이 호출되고 있음을 알 수 있다.  

```python
print('r : %r' % v) # r : Vector(3, 4)
print('s : %s' % v) # s : Vector(3, 4)
print('!r : {!r}'.format(v)) # !r : Vector(3, 4) 
print('!s : {!s}'.format(v)) # !s : Vector(3, 4)
```
