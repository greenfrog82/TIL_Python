# urllib

## [urllib.quote(string[, safe])](https://docs.python.org/2/library/urllib.html#urllib.quote)

[URL Encoding](https://github.com/greenfrog82/study/blob/master/web/url_encoding.md)을 수행한다. 

### Parameter(s)

#### string

`string`파라메터로 전달 된 `special character`들을 `%xx`escape 문자로 치환한다. **알파벳, 숫자 그리고 '_.-'문자들**은 치환되지 않는다.  

#### safe (option)

`safe`파라메터는 옵션으로, 특정 캐릭터를 치환하지 않는다.  
**기본값은 '/'**이다.  

### Example

다음은 각각 '~'문자와 한글을 `quote`함수를 통해 URL에 적합한 형태로 치환한다. 

```python
>>> urllib.quote('/~connolly/')
'/%7Econnolly/'
>>> urllib.quote('/~connolly/아이콘.png')
'/%7Econnolly/%EC%95%84%EC%9D%B4%EC%BD%98.png'
```

다음은 `safe`파라메터를 이용해서 앞선 예제에서 치환했던 문자들을 치환하지 않도록한다. 

```python
>>> urllib.quote('/~connolly/', '~/')
'/~connolly/'

>>> urllib.quote('/~connolly/아이콘.png', '~/아이콘')
'/~connolly/\xec\x95\x84\xec\x9d\xb4\xec\xbd\x98.png'
```

마지막으로, 알파벳, 숫자 그리고 '_.-'문자들을 인코딩하지 않는지 확인해보자. 

```python
>>> urllib.quote('abc123_.-')
'abc123_.-'
```

## [urllib.quote_plus(string[, safe])](https://docs.python.org/2/library/urllib.html#urllib.quote_plus)

`urllib.quote`와 비슷하지만, **`HTML Form`에 대한 쿼리 스트링을 생성할 때, 공백을 `%20`값으로 인코딩하지 않고 `+`로 인코딩한다.** 이는 W3C의 표준으로 다음과 같이 명시하고 있다.  

>application/x-www-form-urlencoded  
This is the default content type. Forms submitted with this content type must be encoded as follows:
>
>1. Control names and values are escaped. Space characters are replaced by `+', and then reserved characters are escaped as described in [RFC1738], section 2.2: Non-alphanumeric characters are replaced by `%HH', a percent sign and two hexadecimal digits representing the ASCII code of the character. Line breaks are represented as "CR LF" pairs (i.e., `%0D%0A').

### Parameter(s)

#### string

`string`파라메터로 전달 된 `special character`들을 `%xx`escape 문자로 치환한다. **알파벳, 숫자 그리고 '_.-'문자들**은 치환되지 않는다.  
`urllib.quote`와 달리 공백은 `+`로 치환하고, `/`이 safe의 기본값이 아니기 때문에 UTF-8 인코딩을 기준으로 `%2F`로 치환된다. 

#### safe (option)

`safe`파라메터는 옵션으로, 특정 캐릭터를 치환하지 않는다.  

### Example

앞서 설명한바와 같이 공빅을 `+`로 인코딩하는지 확인해보자.   
다음과 같이 공백이 `+`로 인코딩 된 것을 확인할 수 있다. 

```python
>>> urllib.quote_plus('version=Python 2.x')
'version%3DPython+2.x'
```

이번에는 `/`은 어떻게 인코딩 되는지 확인해보자.   
앞서 설명한 것과 같이 `/`은 `safe`인자의 기본값이 아니기 때문에 `%2F`로 인코딩 된 것을 확인할 수 있다. 

```python
>>> urllib.quote_plus('version=Python 2.x/Python 3.x')
'version%3DPython+2.x%2FPython+3.x'
```

다음 예제를 통해, `urllib.quote`와 동일하게 알파벳, 숫자 그리고 '_.-'문자들을 인코딩하지 않는것을 확인할 수 있다. 

```python
>>> urllib.quote('abc123_.-')
'abc123_.-'
```

## [urllib.urlencode](https://docs.python.org/2/library/urllib.html#urllib.urlencode)

mapping object 또는 두개의 요소로 구성 된 tuple을 요소로 갖는 sequence를 `percent-encoded string`으로 변환하며, `urlopen()`의 `data`파라메터에 전달하기 적합한 형태이다. 이 함수는 form fields의 dictionary를 POST 요청으로 전달할 때 유용하다. 해당 함수의 결과는 `&`문자로 분리된 `key-value`짝이다. 이때 `key`와 `value`값은 `quote_plus()`함수에 의해 인코딩된다.   


### Parameter(s)

#### query

url encoding을 적용하기 위한 `mapping object` 또는 `sequence`

#### doseq (option)

해당 옵션이 `True`인경우 특정 key에 value로 `sequence`가 전달되었을 때, 해당 key에 대해서 `&`로 분리된 `key=value`쌍을 반환한다. `False`인 경우는 `sequence`를 통째로 encoding하며, default값이다. 


### Example

일반적으로 dictionary와 tuple을 `query`파라메터로 전달해보자.  

```python
In [2]: from urllib import urlencode

In [3]: query = {
   ...: 'name': 'greenfrog',
   ...: 'job': 'developer',
   ...: }

In [4]: urlencode(query)
Out[4]: 'job=developer&name=greenfrog'

In [7]: query = (('name', 'greenfrog'), ('job', 'developer'))

In [8]: urlencode(query)
Out[8]: 'name=greenfrog&job=developer'
```

'likes'키에 sequence를 전달해보자. 
결과를 확인해보면 괄호를 포함해 sequence안의 값을 모두 인코딩한것을 알 수 잇다. 또한 `doseq`파라메터의 기본값은 `False`이므로 둘의 값이 동일한 것을 확인할 수 있다. 

```python
In [16]: query = {
    ...: 'name': 'greenfrog',
    ...: 'likes': ('programming',10),
    ...: }

In [21]: urlencode(query)
Out[21]: 'name=greenfrog&likes=%28%27programming%27%2C+10%29'

In [23]: urlencode(query, False)
Out[23]: 'name=greenfrog&likes=%28%27programming%27%2C+10%29'
```

위 예제에서 `doseq`값을 `True`로 전달해보자. 다음과 같이 해당 key에 대해서 `&`로 분리된 `key=value`쌍을 반환하는것을 확인할 수 있다. 

```python
In [24]: urlencode(query, True)
Out[24]: 'name=greenfrog&likes=programming&likes=10'
```

# Reference

* [urllib 2.7.15](https://docs.python.org/2/library/urllib.html)
* [W3C - 17.13.4 Form content types](https://www.w3.org/TR/html4/interact/forms.html#h-17.13.4.1)
* [URL encoding the space character: + or %20?](https://stackoverflow.com/questions/1634271/url-encoding-the-space-character-or-20)
