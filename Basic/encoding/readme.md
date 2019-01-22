# Unicode 

## On Python 2.7

```python
>>> python = '파이썬'
>>> python
'\xed\x8c\x8c\xec\x9d\xb4\xec\x8d\xac'

>>> python[0]
'\xed'

>>> print python[0]
�

>>> print python[:3]
파

>>> eng_python = 'Python'
>>> eng_python[0]
'P'

>>> print eng_python[0]
P

>>> print eng_python[:3]
Pyt

>>> u_python = u'파이썬'
>>> u_python
u'\ud30c\uc774\uc36c'

>>> u_python[0]
u'\ud30c'

>>> print u_python[0]
파
```

## On Python 3.x



# Reference

* [파이썬 2와 유니코드](https://www.slideshare.net/LeeSeongjoo/2-17395073)
* [Python 2.x 한글 인코딩 관련 정리](https://libsora.so/posts/python-hangul/)
* [파이썬에서 한글이 깨진다고요? – 파이썬의 한글 입출력과 인코딩에 대해](https://soooprmx.com/archives/4912)

