# side_effect

`mock`의 `side_effect`속성은 mocking한 함수가 호출될 때, 특정 함수가 호출되게 하거나, iterable한 객체를 iterate하거나 예외를 발생시킬 수 있다. 

## side_effect with function

만약, `side_effect`속성에 함수를 전달한다면, 전달한 함수가 [DEFAULT](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.DEFAULT)를 반환하지 않는한 mock함수를 호출할 때 `side_effect`속성으로 전달한 함수가 호출된다.  

다음 예제를 보면 명시적으로 이해가 될 것이다. 

```python
>>> from unittest.mock import Mock
>>> mock = Mock(side_effect=lambda x: x)
>>> mock(10)
10 
```

그럼 앞서 잠시 언급한 [DEFAULT](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.DEFAULT)을 반환하도록해보자.  
```python
>>> from unittest.mock import Mock, DEFAULT
>>> mock = Mock(side_effect = lambda: DEFAULT)
>>> mock()
<Mock name='mock()' id='4553857288'>
```

결과를 보면, 그냥 mock을 호출했을 때와 동일하다. 이는 [DEFAULT](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.DEFAULT)가 `return_value`속성으로 할당된 값을 반환하는 역할을 하기 때문이다.  

위 예제에 `return_value`속성을 추가하여 테스트해보자. `return_value`에 할당된 값이 잘 출력되고 있음을 알 수 있다.  

```python
>>> mock = Mock(side_effect = lambda: DEFAULT, return_value=100)
>>> mock()
100
```

## side_effect with iterables

`side_effect`에 `iterable`을 전달하면 `mock`이 호출될때마다 다음 `iterable`의 다음 원소 값을 반환하도록 할 수 있다. 이러한 방법은 테스트 함수안에서 `mock`이 여러번 호출 될 때 **서로 다른 반환값을 전달하도록 하기위해서** 사용될 수 있을 것이다.   

먼저 제일 간단하게 리스트를 전달해보자. `mock`이 호출 될 때 마다 리스트의 다음 원소들이 반환되는것을 확인할 수 있다.  

```python
>>> mock = Mock(side_effect=[1, 2, 3])
>>> mock()
1
>>> mock()
2
>>> mock()
3
```

앞서 `side_effect`에 함수를 전달하는 방식과 `iterable`을 함께 사용하면, 단순히 리스트의 값을 반환하는 수준이 아닌 `mock`에 특정 파라메터가 전달 될 때마다 특정 값이 반환되도록도 할 수 있다.   

```python
>>> vals = {(1, 2): 1, (2, 3): 2}
>>> def side_effect(*args):
...     return vals[args]
>>> mock = Mock(side_effect=side_effect)
>>> mock(1,2)
1
>>> mock(2,3)
2
```

## Raising exception

`side_effect`에 예외클래스 또는 인스턴스를 전달하면 `mock`이 호출되는 시점에 예외가 발생한다.  
```python
>>> mock = Mock(side_effect=Exception)
>>> mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/a201808045/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 951, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/Users/a201808045/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 1007, in _mock_call
    raise effect
Exception

>>> mock = Mock(side_effect=Exception('foo'))
>>> mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/a201808045/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 951, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/Users/a201808045/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 1007, in _mock_call
    raise effect
Exception: foo

foo
```

# Reference

* [Raising exceptions with mocks](https://docs.python.org/3/library/unittest.mock-examples.html#raising-exceptions-with-mocks)
* [Side effect functions and iterables](https://docs.python.org/3/library/unittest.mock-examples.html#side-effect-functions-and-iterables)
* [side_effect](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect) 