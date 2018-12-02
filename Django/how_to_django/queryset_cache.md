# [Caching and QuerySets](https://docs.djangoproject.com/en/2.1/topics/db/queries/#caching-and-querysets)

`QuerySet`은 데이터베이스에 최소한으로 접근한기 위해 `cache`를 포함한다. `QuerySet`의 `cache`에대한 이해는 효과적인 코드를 작성하는데 아주 중요하다.  

`QuerySet`이 새롭게 생성되면 `cache`는 비어있는 상태이다. `QuerySet`이 데이터베이스 쿼리가 나가게되면 `cache`에 해당 쿼리 결과를 `cache`에 저장한 후 반환한다. 이후 `QuerySet`은 데이터베이스에 쿼리를 보내지 않고 `cache`되었던 결과를 반환한다.  

```python
In [1]: from django.db import connection

In [2]: [article.content for article in Article.objects.all()]
Out[2]: ['a', 'b']

In [3]: [article.content for article in Article.objects.all()]
Out[3]: ['a', 'b']

In [4]: len(connection.queries)
Out[4]: 2
```

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

# Reference

* [Django qeurysets have a cache](http://blog.etianen.com/blog/2013/06/08/django-querysets/)
* [Database access optimization](https://docs.djangoproject.com/en/2.1/topics/db/optimization/)