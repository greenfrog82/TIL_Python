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

