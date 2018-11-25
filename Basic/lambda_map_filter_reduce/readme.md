# lambda, map, reduce and filter

## lambda

`lambda`는 Functional Programming에 익숙한 개발자라면 누구나 알고있는 표현식이다.  
이를 간단히 설명하면, 전달받은 함수에 따라 동작을 달리하는 코드 템플릿이 있다고 할 때 재활용 할 필요가 없는 함수가 있다고 하 때 이러한 표현식을 이용하면 코드를 좀 더 간단히 표현할 수 있다.   

lambda 표현식은 다음과 같다.

>lambda argument_list: expression

앞서 `lambda` 표현식의 정의를 보면 `argument_list`로 전달 된 인자들이 `expression`으로 전달되는 구조이다.

### Example

다음 에제는 `lambda`를 통해 덧셈을 하는 함수를 만든다. 

[ex_lambda.py](./ex_lambda.py)
```python
>>> sum = lambda x, y: x + y
>>> sum(3, 4)
7
```

다음과 같이 `lambda`를 정의할 때 `argument_list`를 정의하지 않으면 인자를 전달받지 않는 `lambda`가 정의된다. 

[ex_lambda.py](./ex_lambda.py)
```python
>>> one = lambda: 1
>>> one()
1
```

## map

`map`함수는 기존에 존재하는 `sequence`를 통해 새로운 `list`객체를 생성한다.  

>r = map(func, seq)

### Parameter

* **func** : `seq` 파라메터로 전달 된 `sequence`의 요소에 적용하고자 하는 로직을 포함하고 있는 함수이다. 
* **seq** : `map`을 통해 생성하고자는 새로운 `list`에 소스가 되는 `sequence`객체.  
`seq`는 `comma`로 구분해서 여러개의 `sequence`객체를 전달할 수 있는데, 반드시 같은 길이의 `sequence`객체를 전달해야한다. 

### Example

```python
>>> list(map(lambda x: x+1, range(10)))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

앞서 `map`은 여러개의 `sequence`객체를 전달할 수 있다고 했다. 그 이유는 각 `sequence`객체의 요소들이 `func`인자의 각각의 인자로 전달되기 때문이다.

다음 예제를를 확인하자. 
`map`함수로 전달되는 `sequence`객체가 2개이지만, `func`함수의 인자가 하나이기 때문에 에러가 발생하였다. 

```python
>>> list(map(lambda x: x+1, range(2), range(3, 5)))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: <lambda>() takes 1 positional argument but 2 were given

<lambda>() takes 1 positional argument but 2 were given
```

이번에는 전달하는 `sequence`의 길이를 달리해보자.  
에러가 발생하진 않고, 작은 길이의 `sequence`를 기준으로 `list`를 생성한다.  

```python
>>> list(map(lambda x,y: x+y, range(1), range(3, 5)))
[3]
```

마지막으로 같은 길이의 `sequence`를 전달했을 경우의 예제를 확인해보자.  

```python
>>> list(map(lambda x,y: x+y, range(2), range(3, 5)))
[3, 5]
```













## Reference

* [Lambda, filter, reduce and map](https://www.python-course.eu/lambda.php)