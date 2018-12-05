# [exists()](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.exists)

`exists`메소드는 `QuerySet`이 결과를 가지고 있다면 **True**를 반환하고, 그렇지 않으면 **False**를 반환한다. 이 메소드는 가능한 간단하고 빠른 쿼리를 실행하지만 일반적인 쿼리와 거의 비슷하다.  

`exists`메소드는 쿼리 결과가 큰 경우 해당 쿼리의 존재여부를 확인하는데 유용하다.  

예를들어, 쿼리의 결과를 확인하기 위해 다음과 같이 코드를 작성해보자. 

```python
>>> qs = Article.objects.all()
>>> if qs:
...     print('test')
...
...
test
>>> connection.queries[-1]
{'sql': 'SELECT "app_model_article"."id", "app_model_article"."content", "app_model_article"."created_date", "app_model_article"."updated_date" FROM "app_mo
del_article"', 'time': '0.000'}
```

위 결과를 보면, 해당 쿼리의 결과를 확인하기 위해 불필요한 필드들을 쿼리에 포함하고 있으며 테이블의 모든 결과를 조회해오는 것을 알 수 있다.  
예제에 사용한 테이블에 데이터가 별로 없어서 쿼리에 걸린시간이 0초에 가깝지만, 만약 데이터가 많았다면 많은 시간을 사용했을 것이다. 

이번에는 다음과 같이 `exists`메소드를 사용해보자. 

```python
>>> qs = Article.objects.all()
>>> if qs.exists():
...     print('success')
...
...
success
>>> connection.queries[-1]
{'sql': 'SELECT (1) AS "a" FROM "app_model_article"  LIMIT 1', 'time': '0.000'}
```

위 결과르 보면, 해당 쿼리의 결과가 존재하는지 확인하기 위해 테이블의 모든 데이터를 조회하지 않고 **단 하나**의 데이터만을 조회한다. 
`exists`메소드는 위와같은 원리로 효율적으로 쿼리의 결과가 존재하는지를 확인한다.  

`exists`메소드를 사용할 때 한가지 주의할 점이있다.  
만약, 쿼리의 결과가 존재하는지 확인한 후 해당 데이터를 사용해야하는 경우 `exists`메소드를 사용하면 오히려 쿼리가 한번 더 나가는 문제가 있기 때문이다.  

다음 예제를보자.  
QuerySet의 데이터 존재여부를 확인한 후, 데이터가 존재할 때 데이터를 사용하고있다.  
쿼리 결과를 확인해보면, `exists`메소드를 처리하면서 쿼리가 한번 나가고, 데이터를 사용할 때 쿼리가 **한번 더** 나가는것을 확인할 수 있다. 

```python
In [2]: articles = Article.objects.all()

In [3]: if articles.exists():
   ...:     articles[0].updated_date

In [4]: len(connection.queries)
Out[4]: 2

In [5]: connection.queries[0]
Out[5]: {'sql': 'SELECT (1) AS "a" FROM "app_model_article"  LIMIT 1', 'time': '0.000'}

In [6]: connection.queries[1]
Out[6]:
{'sql': 'SELECT "app_model_article"."id", "app_model_article"."content", "app_model_article"."created_date", "app_model_article"."updated_date" FROM "app_model_article"  LIMIT 1',
 'time': '0.000'}
```

하지만, 다음과 같이 if문에서 QuerySet을 evaluation시키면 쿼리가 나가면서 cache되고 이후 해당 QuerySet에 접근할 때는 cache된 데이터를 사용하기 때문에 쿼리가 **한번만** 나가는 것을 확인할수있다. 
```python
In [1]: from django.db import connection

In [2]: articles = Article.objects.all()

In [3]: if articles:  # 여기서 QuerySet이 evaluation되면서 cache된다. 
   ...:     articles[0].updated_date # 여기서 cache된 데이터를 사용한다. 

In [4]: len(connection.queries)
Out[4]: 1
```

# Reference

* [Using Django querysets effectively](http://blog.etianen.com/blog/2013/06/08/django-querysets/)