# sorted function vs sort method

[sorted built-in function](https://docs.python.org/3/library/functions.html#sorted)과 [sort method](https://docs.python.org/3/library/stdtypes.html#list.sort)의 차이점에 대해서 알아보자. 

## [sorted built-in function](https://docs.python.org/3/library/functions.html#sorted)

`sorted build-in function`은 `iterable`객체를 전달받아 **오름차순으로 정렬**된 `list`객체를 반환한다.  

```python
>>> arr = [1,3,2,5,4]
>>> id(arr)
4482253896
>>> arr_ = sorted(arr)
>>> arr_
[1, 2, 3, 4, 5]
>>> id(arr_)
4483232072
```

## [sort method](https://docs.python.org/3/library/stdtypes.html#list.sort)

`sort method`는 `list`클래스의 method로 해당 객체의 데이터를 **오름차순으로 정렬**한다.  

```python
>>> arr = [1,3,2,5,4]
>>> id(arr)
4482253896
>>> arr.sort()
>>> arr
[1, 2, 3, 4, 5]
>>> id(arr)
4482253896
```

## Common

`sorted build-in function`과 `sort method`는 앞서와 같이 정렬된 새로운 객체를 반환하느냐 아니면 해당 객체의 데이터를 정렬하느랴와 `iterable`을 인자로 받냐 그렇지 않냐의 차이점을 제외하면 전달 받는 파라메터와 결과는 동일하다.

이들 둘의 공통 된 파라메터에 대해서 `sorted build-in function`을 통해 설명한다. 

### key keyword parameter

`key`키워드 파라메터는 정렬을 하기 위한 값을 전달받아 해당 값을 정렬하고자하는 형태로 반환하기 위한 `function`을 전달받는다. 이러한 방법은 정렬하고자 하는 각각의 데이터에 대해서 정확히 한번만 호츌되기 때문에 빠르다.   

다음 예제는 `key` 키워드 파라메터에 `str.lower`를 전달하여 각각의 데이터를 소문자로 만든 후 **오름차순**으로 정렬한다. 

```python
>>> sorted("This is a test string from Andrew".split(), key=str.lower)
['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']
```

다음 예제는 `key` 키워드 파라메터에 학생의 나이를 반환하는 람다함수를 전달하여 학생들의 나이를 **오름차순**으로 정렬한다. 

```python
>>> student_tuples = [
...     ('john', 'A', 15),
...     ('jane', 'B', 12),
...     ('dave', 'B', 10),
... ]
>>> sorted(student_tuples, key=lambda student: student[2])
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
>>>
```

앞서 작성했던 예제(학생을 나이순으로 정렬)를 [operator](https://docs.python.org/3/library/operator.html#module-operator)모듈의 다음 함수들을 활용하면 복잡한 람다함수를 작성하지 않고 쉽게 처리할 수 있다.  
[operator.itemgetter](https://docs.python.org/3/library/operator.html#operator.itemgetter)을 이용해서 앞선 예제를 수정해보자.

```python
>>> sorted(student_tuples, key=itemgetter(2))
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
```

`operator.itemgetter`는 복수개의 index를 전달 받을 수 있는데 다음과 같이 **이름**으로 먼저 정렬하고, **나이**로 정렬이 가능하다.

```python
>>> sorted(student_tuples, key=itemgetter(1, 2))
[('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
```

### Ascending and Descending

`sorted build-in function`과 `sort method`는 기본적으로 **오름차순 정렬**을 한다. 이는 `reverse` 키워드 파라메터의 기본값이 `False`이기 때문인데, 이를 `True`로 바꾸면 **내림차순 정렬**을한다.  
앞선 예제를 나이에 대해서 **내림차순 정렬**을 해보면 다음과 같다.  

```python
>>> sorted(student_tuples, key=itemgetter(2), reverse=True)
[('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
```

# Reference

* [sorted built-in function](https://docs.python.org/3/library/functions.html#sorted)
* [sort method](https://docs.python.org/3/library/stdtypes.html#list.sort)
* [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html#sortinghowto)
