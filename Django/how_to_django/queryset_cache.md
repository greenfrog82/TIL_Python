# [Caching and QuerySets](https://docs.djangoproject.com/en/2.1/topics/db/queries/#caching-and-querysets)

`QuerySet`은 데이터베이스에 최소한으로 접근한기 위해 `cache`를 포함한다. `QuerySet`의 `cache`에 대한 이해는 효과적인 코드를 작성하는데 아주 중요하다.  

`QuerySet`이 새롭게 생성되면 `cache`는 비어있는 상태이다. `QuerySet`이 실행되면, `QuerySet`의 `cache`에 해당 쿼리 결과를 저장한 후 반환한다. 이후 `QuerySet`을 통해 데이터에 접근을 시도하면 더 이상 `QuerySet`의 실행하지 않고 `cache`되었던 결과를 반환한다.  

다음 예제를보자. 각각 생성 된 두개의 `QuerySet`을 실행한 후 `list comprehension`을 통해 두개의 `list`를 생성하고 있다. 이 경우 완전히 동일한 데이터베이스 쿼리가 두번 나간다. 또한 각각 데이터베이스를 질의하는 사이에 데이터가 추가되거나 삭제될 수 있기 때문에, 이 두 `list`는 서로 다른 결과를 반환 할 수 있다.  

```python
In [1]: from django.db import connection

In [2]: [article.content for article in Article.objects.all()]
Out[2]: ['a', 'b']

In [3]: [article.content for article in Article.objects.all()]
Out[3]: ['a', 'b']

In [4]: len(connection.queries)
Out[4]: 2
```

앞서와 같은 문제를 피하기 위해서, `QuerySet`의 `cache`를 활용해보자. 우선 `cache`를 사용하기 위해서는 `QuerySet`을 별도 변수에 할당해두었다가 재사용해야한다.   
다음 예제를보자. `qs`라는 변수에 `QuerySet`을 할당한 후 이를 통해 두개의 `list`를 생성하고 있다.   
위 예제의 경우 데이터베이스로 쿼리를 한번 요청하고, 응답받은 결과를 `QueySet`의 `cache`에 저장한다. 이후 다음 `list`를 생성할 때는 캐쉬된 데이터를 재사용하기 때문에 쿼리가 더 이상 나가지 않는다.   

```python
In [1]: from django.db import connection

In [2]: qs = Article.objects.all()

In [3]: [article.content for article in qs]
Out[3]: ['a', 'b']

In [4]: [article.content for article in qs]
Out[4]: ['a', 'b']

In [5]: len(connection.queries)
Out[5]: 1
```

## When QuerySets are not cached

`QuerySet`을 변수에 할당한 후 사용한다고 해서 언제나 쿼리 결과를 캐쉬하는것은 아니다. `QueySet`의 일부에 대해서만 쿼리를 실행하면 `QuerySet`은 쿼리 결과를 캐쉬하지 않는다. 좀 더 구체적으로 이야기하면, **배열의 slice 또는 index를 통해 실행 된 결과는 캐쉬되지 않는다.**   

예를들어, 다음과 같은 경우 데이터베이스의 모든 쿼리결과에 대한 `QuerySet`에서 1번째 인덱스의 결과를 두번 출력하고있다. 이와같은 경우 쿼리가 각각 두번 실행된다. 

```python
In [1]: from django.db import connection

In [2]: qs = Article.objects.all()

In [3]: qs[1]
Out[3]: <Article: Article object (2)>

In [4]: qs[1]
Out[4]: <Article: Article object (2)>

In [5]: len(connection.queries)
Out[5]: 2
```

위 예제에서 추가적으로 slice를 통해 쿼리결과를 가져와보자.   
역시 쿼리가 한번 더 실행되었다. 

```python
In [6]: qs[1:]
Out[6]: <QuerySet [<Article: Article object (2)>]>

In [7]: len(connection.queries)
Out[7]: 3
```

이번에는 `QuerySet`의 쿼리 전체를 실행한 후 앞서 index와 slice를 각각 사용해서 데이터에 접근해보자.   
이 경우, 모든 쿼리를 실행시키면 쿼리결과가 `cache`된다. 따라서 쿼리는 단 한번만 실행되었음을 알 수 있다. 

```python
In [1]: from django.db import connection

In [2]: qs = Article.objects.all()

In [3]: list(qs)
Out[3]: [<Article: Article object (1)>, <Article: Article object (2)>]

In [4]: len(connection.queries)
Out[4]: 1

In [5]: qs[1]
Out[5]: <Article: Article object (2)>

In [6]: len(connection.queries)
Out[6]: 1

In [7]: qs[1]
Out[7]: <Article: Article object (2)>

In [8]: len(connection.queries)
Out[8]: 1

In [9]: qs[1:]
Out[9]: [<Article: Article object (2)>]

In [10]: len(connection.queries)
Out[10]: 1
```

다음 예제도 위 예제와 마찬가지로 전체 쿼리를 실행 시킨 후 `cache`된 데이터를 재사용하고 있다. 

```python
In [1]: from django.db import connection

In [2]: qs = Article.objects.all()

In [3]: list(qs)
Out[3]: [<Article: Article object (1)>, <Article: Article object (2)>]

In [4]: len(connection.queries)
Out[4]: 1 

In [5]: [article.content for article in qs]
Out[5]: ['a', 'b']

In [6]: len(connection.queries)
Out[6]: 1
```

# Reference

* [Django qeurysets have a cache](http://blog.etianen.com/blog/2013/06/08/django-querysets/)
* [Database access optimization](https://docs.djangoproject.com/en/2.1/topics/db/optimization/)