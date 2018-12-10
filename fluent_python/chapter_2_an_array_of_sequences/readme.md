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
