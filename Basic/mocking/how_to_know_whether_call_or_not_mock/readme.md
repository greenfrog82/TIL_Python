# How to know whether mock function call or not

`Python 3.7`

앞서 [Import Problem](../import_problem)을 보면 Mocking한 함수가 정상적으로 호출되는지를 확인하지 않는 테스트코드를 작성하는 바람에 Mocking이 잘못된 것을 코드를 살펴서 알 수 있었다. 

그렇다면 어떻게하면 Mocking한 함수가 호출되는지 확인 할 수 있을까? 일단 `Python 3.7`에서는 다음 7가지 함수를 통해 이를 확인할 수 있다.  

* assert_called(*args, **kwargs)
* assert_called_once(*args, **kwargs)
* assert_called_with(*args, **kwargs)
* assert_called_once_with(*args, **kwargs)
* assert_any_call(*args, **kwargs)
* assert_has_calls(calls, any_order=False)
* assert_not_call(*args, **kwargs)

## assert_called(*args, **kwargs)

Mocking된 함수가 최소한 한번 호출되었는지 확인한다.   
New in version 3.6.

Mocking된 함수가 최소한 한번 호출 된 경우.

```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock.method()
<Mock name='mock.method()' id='4497228912'>
>>> mock.method.assert_called()
```

Mocking된 함수가 호출되지 않은 경우.

```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock.method.assert_called()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 792, in assert_called
    raise AssertionError(msg)
AssertionError: Expected 'method' to have been called.

Expected 'method' to have been called.
```

## assert_called_once(*args, **kwargs)

Mocking된 함수가 단 한번 호출된 것을 확인한다. 
New in version 3.6

```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock.method()
<Mock name='mock.method()' id='4484048768'>
>>> mock.method()
<Mock name='mock.method()' id='4484048768'>
>>> mock.method.assert_called_once()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 801, in assert_called_once
    raise AssertionError(msg)
AssertionError: Expected 'method' to have been called once. Called 2 times.

Expected 'method' to have been called once. Called 2 times.
```

## assert_called_with(*args, **kwargs)

Mocking된 함수가 특정 방법으로 호출되었는지 확인한다. 

```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock.method(1, 2, 3, test='wow')
<Mock name='mock.method()' id='4486641648'>
>>> mock.method.assert_called_with(1, 2, 3, test='wow')

>>> mock.method.assert_called_with(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 820, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: method(1)
Actual call: method(1, 2, 3, test='wow')

Expected call: method(1)
Actual call: method(1, 2, 3, test='wow')
```

## assert_called_once_with(*args, **kwargs)

Mocking된 함수가 특정한 방법으로 한 번 호출되었는지 확인한다. 

```python
>>> mock = Mock(return_value=None)
>>> mock
<Mock id='4496433616'>
>>> mock('foo', bar='baz')
>>> mock.assert_called_once_with('foo', bar='baz')
>>> mock('foo', bar='baz')
>>> mock.assert_called_once_with('foo', bar='baz')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 830, in assert_called_once_with
    raise AssertionError(msg)
AssertionError: Expected 'mock' to be called once. Called 2 times.

Expected 'mock' to be called once. Called 2 times.
```

## assert_any_call(*args, **kwargs)

Mocking된 함수가 특정 방법을 한번이라도 호출되었는지 확인한다.  

```python
>>> mock = Mock()
>>> mock(1, 2, 3)
<Mock name='mock()' id='4490909792'>
>>> mock(test='wow')
<Mock name='mock()' id='4490909792'>
>>> mock.assert_any_call(1, 2, 3)
>>> mock(1, 2, 3)
<Mock name='mock()' id='4490909792'>
>>> mock.assert_any_call(1, 2, 3)
>>> mock.assert_any_call(1, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 882, in assert_any_call
    ) from cause
AssertionError: mock(1, 2) call not found

mock(1, 2) call not found
```

## assert_has_calls(calls, any_order=False)

Mocking된 함수가 특정 방법들로 호출되었는지 확인한다. `any_order`의 기본값은 `False`로 호출 된 순서까지 확인한다. 해당 값은 `True`로 바꾸면 호출된 순서를 확인하지 않는다.  

```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock(1)
<Mock name='mock()' id='4495578448'>
>>> mock(2)
<Mock name='mock()' id='4495578448'>
>>> mock(3)
<Mock name='mock()' id='4495578448'>
>>> mock(4)
<Mock name='mock()' id='4495578448'>

>>> from unittest.mock import call
>>> calls = [call(1), call(2)]
>>> mock.assert_has_calls(calls)

>>> calls = [call(2), call(1)]
>>> mock.assert_has_calls(calls)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 852, in assert_has_calls
    ) from cause
AssertionError: Calls not found.
Expected: [call(2), call(1)]
Actual: [call(1), call(2), call(3), call(4)]

Calls not found.
Expected: [call(2), call(1)]
Actual: [call(1), call(2), call(3), call(4)]

>>> mock.assert_has_calls(calls, any_order=True)
```

## assert_not_call(*args, **kwargs)

Mocking된 함수가 호출되지 않았음을 확인한다.   

```python
>>> mock = Mock()
>>> mock.assert_not_called()

>>> mock(1)
<Mock name='mock()' id='4499615248'>
>>> mock.assert_not_called()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/unittest/mock.py", line 783, in assert_not_called
    raise AssertionError(msg)
AssertionError: Expected 'mock' to not have been called. Called 1 times.

Expected 'mock' to not have been called. Called 1 times.
```