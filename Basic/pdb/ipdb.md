# ipdb를 통해서 파이썬 코드 디버깅하기

`ipdb`는 `pdb`모듈과 같은 인터페이스를 제공하지만 좀 더 좋은 traceback과 syntax highlighting 그리고 tab completion을 제공한다. 

`ipdb`를 통해 파이썬 코드를 디버깅하는 방법은 `pdb`를 사용하는 방법과 동일하다. 따라서, 디버깅하는 방법은 [pdb.md](./pdb.md)문서를 참고하기 바란다.   

여기서는 ipdb를 통해 확장 된 기능 몇가지를 알아보도록 하자. 

## ipdb.set_trace(context=number)

일반적으로 `ipdb.set_trace()`를 호출하면 다음과 같이 3개의 라인을 보여준다. 

```python
> /Users/greenfrog/develop/TIL_Python/Basic/pdb/src/example.py(18)<module>()
     17
---> 18 num1 = 100
     19
```

하지만, `context`파라메터를 이용하면 출력하고자하는 라인을 지정할 수 있다. 예를들어 `ipdb.set_trace(context=5)`를 사용하면 다음과 같이 5개의 라인을 보여준다. 

```python
> /Users/greenfrog/develop/TIL_Python/Basic/pdb/src/example.py(21)<module>()
     19
     20 ipdb.set_trace(context=5)
---> 21 num2 = 5
     22
     23 result = calc('*', num1, num2)
```

## with launch_ipdb_on_exception()

with와 함께 `launch_ipdb_on_exception()`을 사용하면 해당 스콥의 코드에서 `exception`이 발생하면 디버깅 모드로 진입한다. 하지만 `set_trace()`와 달리 디버깅이 진행되지는 않는다.  

```python
from ipdb import launch_ipdb_on_exceptionf

... 

with launch_ipdb_on_exception():
    ret = 10 / 0

ZeroDivisionError('division by zero')
> /Users/greenfrog/develop/TIL_Python/Basic/pdb/src/example.py(20)<module>()
     19 with launch_ipdb_on_exception():
---> 20     ret = 10 / 0
     21
```

# Reference

* [ipdb](https://github.com/gotcha/ipdb)