# [Underscores in Numeric Literals](https://www.python.org/dev/peps/pep-0515/)

`Python 3.6`

숫자를 다루는 표현식에서 `underscore`를 사용하면 숫자들을 그룹핑해서 구분할 수 있다. 

```python
# grouping decimal numbers by thousands
amount = 10_000_000.0

# grouping hexadecimal addresses by words
addr = 0xCAFE_F00D

# grouping bits into nibbles in a binary literal
flags = 0b_0011_1111_0100_1110

# same, for string conversions
flags = int('0b_1111_0000', 2)
```
