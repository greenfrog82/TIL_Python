# index vs find method of string

`Python 2.7.15` `Python3.7.0`

파이썬의 문자열에는 `index`와 `find`메소드가 있다.   
각각 원본 문자열에 대해서 파라메터로 전달받은 서브문자열이 매칭되는 인덱스를 반환한다. 이때 반환되는 인덱스는 파라메터로 전달받은 서브문자열의 첫글자와 매칭되는 원본 문자열의 인덱스이다.  
이 두 메소드의 파라메터는 다음과 같이 동일하고, 의미 역시 동일하다. 

> str.find(sub[, start[, end]])  
str.index(sub[, start[, end]])

### Parameter(s)

* **sub** : str에서 찾고자하는 문자열 또는 문자
* **start** : str에서 `sub`를 찾고자하는 시작위치
* **end** : str에서 `sub`를 찾고자하는 마지막위치

`start`와 `end` 파라메터는 옵션이고 이들의 동작은 `str[start:end]`와 동일하다. 

## Example(s)

```python
>>> str_ = 'Python' 
>>> str_.find('Py')
0
>>> str_.index('Py')
0
```

```python
>>> str_.find('th', 2)
2
>>> str_.index('th', 2)
2
```

```python
>>> str_ = 'abcabc'
>>> str_.find('abc', 0, 3)
0
>>> str_.index('abc', 0, 3)
0
>>> str_.find('abc', 3, 6)
3
>>> str_.index('abc', 3, 6)
3
```

## What is different between find and index?

이와같이 두 메소드는 완전히 동일한 기능을 수행하고 있다. 그렇다면 이렇게 동일한 기능의 메소드를 두 벌 만들어놓은 이유가 뭘까?
**보통 이렇게 함수나 메소드가 동일한 기능을 수행하고 있다면, 호출을 실패했을때 처리가 다른경우가 대부분이다.**  

* `find`메소드의 경우 `sub`파라메터에 매칭되는 문자열을 `str`에서 찾지 못하면 **-1**을 리턴한다. 
* `index`메소드의 경우 `sub`파라메터에 매칭되는 문자열을 `str`에서 찾지 못하면 [ValueError](https://docs.python.org/3.6/library/exceptions.html#ValueError)가 발생한다.

```python
>>> str_ = 'abc'
>>> str_.find('x')
-1
>>> str_.index('x')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: substring not found

substring not found
```

# Reference

* [str.find](https://docs.python.org/3.6/library/stdtypes.html#str.find)
* [str.index](https://docs.python.org/3.6/library/stdtypes.html#str.index)
* [difference between find and index](https://stackoverflow.com/questions/22190064/difference-between-find-and-index)



