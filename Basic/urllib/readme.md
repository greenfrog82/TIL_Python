# urllib

## urllib.quote(string[, safe])

기본적으로 이 함수는 URL의 경로 부분을 치한하기 위한것이다. 

### Parameter(s)

#### string

`string`파라메터로 전달 된 `special character`들을 `%xx`escape 문자로 치환한다. 알파벳, 숫자 그리고 '_.-'문자들은 치환되지 않는다.  

#### safe (option)

`safe`파라메터는 옵션으로, 특정 캐릭터를 치환하지 않는다.  
기본값은 '/'이다.  

### Example

다음은 각각 '~'문자와 한글을 `quote`함수를 통해 URL에 적합한 형태로 치환한다. 

```python
>>> urllib.quote('/~connolly/')
'/%7Econnolly/'
>>> urllib.quote('/~connolly/아이콘.png')
'/%7Econnolly/%EC%95%84%EC%9D%B4%EC%BD%98.png'
quote('/~connolly/') yields '/%7econnolly/'.
```

다음은 `safe`파라메터를 이용해서 앞선 예제에서 치환했던 문자들을 치환하지 않도록한다. 

```python
>>> urllib.quote('/~connolly/', '~/')
'/~connolly/'

>>> urllib.quote('/~connolly/아이콘.png', '~/아이콘')
'/~connolly/\xec\x95\x84\xec\x9d\xb4\xec\xbd\x98.png'
```

# Reference

* [urllib](https://docs.python.org/2/library/urllib.html)