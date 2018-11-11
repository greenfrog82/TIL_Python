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
