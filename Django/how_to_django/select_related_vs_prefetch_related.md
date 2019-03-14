# select_related vs prefetch_related

`Python 3.7`, `Django 2.1`

`select_related`와 `prefetch_related`가 무엇이고, 언제, 왜 사용하는지 알아보자. 이에 대해서 알아보기 위해 사용할 모델은 다음과 같다. 

`Product`모델은 **foreign key relationship**을 가지고 있고, `Category`모델은 **many to many relationship**을 가지고 있다. 

```python
class Category(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    subcategories = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=120)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

그리고 각각 다음과 같은 데이터를 입력해두었다. 

```sql
postgres=# select * from app_model_category;
 id | name | is_active
----+------+-----------
  1 | book | t
  2 | food | t
(2 rows)

postgres=# select * from app_model_product;
 id |   title    | category_id
----+------------+-------------
  1 | Python     |           1
  2 | JavaScript |           1
  3 | Go         |           1
  4 | C#         |           1
  5 | Java       |           1
  6 | Pasta      |           2
  7 | Stake      |           2
  8 | Apple      |           2
  9 | Orange     |           2
 10 | Banana     |           2
(10 rows)
```

## N+1 Query Problem

이제 다음과 같은 코드를 통해 `Product`모델이 가지고 있는 모든 데이터를 출력해보자. 

```python
from app_model.models import Category, Product
from app_model.helpers import debugger_queries


@debugger_queries
def products_list():
    products = []
    for product in Product.objects.all():
        products.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })
    return products
```

위 함수를 `Django Shell`에서 실행해보자.

```python
In [4]: from app_model.examples.n_plus_one_query_problem import products_list

In [5]: products_list()
func:  products_list
queries: 11
took: 0.06s
Out[5]:
[{'id': 1, 'title': 'Python', 'category': 'book'},
 {'id': 2, 'title': 'JavaScript', 'category': 'book'},
 {'id': 3, 'title': 'Go', 'category': 'book'},
 {'id': 4, 'title': 'C#', 'category': 'book'},
 {'id': 5, 'title': 'Java', 'category': 'book'},
 {'id': 6, 'title': 'Pasta', 'category': 'food'},
 {'id': 7, 'title': 'Stake', 'category': 'food'},
 {'id': 8, 'title': 'Apple', 'category': 'food'},
 {'id': 9, 'title': 'Orange', 'category': 'food'},
 {'id': 10, 'title': 'Banana', 'category': 'food'}]
```

출력을 보면 쿼리가 **11번**나간것을 알 수 있다.  
이유는 `products_list`함수에서 쿼리가 다음과 같이 실행되기 때문이다. 주석으로 설명을 추가해두었다. 

```python
...
for product in Product.objects.all(): # 1. Product모델의 모든 데이터를 쿼리한다.  
    products.append({
        'id': product.id,
        'title': product.title,
        'category': product.category.name, # 2. Product모델이 가지고 있는 Category ID를 통해 Category 모델의 데이터를 쿼리한다. 
    })
...
```

실제로 실행된 쿼리의 로그를 보면 다음과 같다. 

```sql
-- 1. Product모델의 모든 데이터를 쿼리한다.  
[2019-03-03 13:22:44.822 UTC][277][5c7bd4f5.115][0]LOG:  duration: 2.567 ms  statement: SELECT "app_model_product"."id", "app_model_product"."title", "app_model_product"."category_id" FROM "app_model_product"

-- 2. Product모델이 가지고 있는 Category ID를 통해 Category 모델의 데이터를 쿼리한다. 
[2019-03-03 13:22:44.830 UTC][277][5c7bd4f5.115][0]LOG:  duration: 3.238 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 1
[2019-03-03 13:22:44.832 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.815 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 1
[2019-03-03 13:22:44.835 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.877 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 1
[2019-03-03 13:22:44.838 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.846 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 1
[2019-03-03 13:22:44.840 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.735 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 1
[2019-03-03 13:22:44.843 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.781 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 2
[2019-03-03 13:22:44.845 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.743 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 2
[2019-03-03 13:22:44.848 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.998 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 2
[2019-03-03 13:22:44.850 UTC][277][5c7bd4f5.115][0]LOG:  duration: 0.899 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 2
[2019-03-03 13:22:44.853 UTC][277][5c7bd4f5.115][0]LOG:  duration: 1.233 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" WHERE "app_model_category"."id" = 2
```

이와같이 쿼리가 1번 실행되고, 루프수만큼 N번 쿼리가 실행되는 문제를 **N+1 Query Problem**이라고 한다. 이는 불필요한 쿼리가 N번 더 실행되기 때문에 성능에 악영향을 끼치기 때문에 피해야한다.

그럼 반대로 `Category`모델에서 `Product`모델의 목록을 가져오는 경우 **N+1 Query Problem**이 발생할까?

```python
@debugger_queries
def category_list():
    category = []
    for product in Category.objects.first().product_set.all():
        category.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })

    return category
```    

위 함수를 실행해보자. 

```python
In [13]: from app_model.examples.n_plus_one_query_problem import category_list
In [14]: category_list()
func:  category_list
queries: 2
took: 0.01s
Out[14]:
[{'id': 5, 'title': 'Java', 'category': 'book'},
 {'id': 4, 'title': 'C#', 'category': 'book'},
 {'id': 3, 'title': 'Go', 'category': 'book'},
 {'id': 2, 'title': 'JavaScript', 'category': 'book'},
 {'id': 1, 'title': 'Python', 'category': 'book'}]
```

출력을 보면 쿼리가 **2번** 실행된 것을 알 수 있다.  
이유는 `category_list`함수에서 쿼리가 다음과 같이 실행되기 때문이다. 주석으로 설명을 추가해두었다. 

```python
@debugger_queries
def category_list():
    category = []
    for product in Category.objects.first().product_set.all(): # 여기서 Category모델의 첫번째 데이터를 가져오기 위해 쿼리를 실행시키고, 가져온 Category모델의 차일드 Product 모델의 데이터를 모두 가져오기 위한 쿼리를 실시킨다. 
        category.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })

    return category
```    

실제로 실행된 쿼리의 로그를 보면 다음과 같다. 

```sql
-- Category.objects.first() 코드의 쿼리
[2019-03-14 12:22:29.003 UTC][29][5c8a4784.1d][0]LOG:  duration: 37.308 ms  statement: SELECT "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_category" ORDER BY "app_model_category"."id" ASC  LIMIT 1
-- Category.objects.first()의 QuerySet을 통한 product_set.all() 코드의 쿼리
[2019-03-14 12:22:29.018 UTC][29][5c8a4784.1d][0]LOG:  duration: 12.917 ms  statement: SELECT "app_model_product"."id", "app_model_product"."title", "app_model_product"."category_id" FROM "app_model_product" WHERE "app_model_product"."category_id" = 1
```

## [select_related](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#select-related)

`select_related`는 쿼리를 할 때 외래키에 대한 데이터까지 한꺼번에 가져온다. 이는 **N+1 Query Problem**을 해결하여 성능을 향상 시키는 방법인데 쿼리를 **단 한번만** 실행시킨다. 

앞서 사용했던 `products_list`함수를 `select_related`를 통해 고친 다음 함수를 통해 문제를 해결해보자.

```python
@debugger_queries
def products_list_with_select_related():
    products = []
    for product in Product.objects.select_related('category').all():
        products.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })
    return products
```

실행 결과를 보면 다음과 같이 쿼리가 1번만 실행된것을 알 수 있다. 

```python
In [4]: products_list_with_select_related()
func:  products_list_with_select_related
queries: 1
took: 0.01s
Out[4]:
[{'id': 1, 'title': 'Python', 'category': 'book'},
 {'id': 2, 'title': 'JavaScript', 'category': 'book'},
 {'id': 3, 'title': 'Go', 'category': 'book'},
 {'id': 4, 'title': 'C#', 'category': 'book'},
 {'id': 5, 'title': 'Java', 'category': 'book'},
 {'id': 6, 'title': 'Pasta', 'category': 'food'},
 {'id': 7, 'title': 'Stake', 'category': 'food'},
 {'id': 8, 'title': 'Apple', 'category': 'food'},
 {'id': 9, 'title': 'Orange', 'category': 'food'},
 {'id': 10, 'title': 'Banana', 'category': 'food'}]
```

실제로 실행된 쿼리의 로그를 보면 다음과 같다. `inner join`을 통해 `Category`관련 데이터까지 모두 쿼리를 한것을 알 수 있다. 

```sql
[2019-03-10 13:37:04.082 UTC][1616][5c8512f8.650][0]LOG:  duration: 5.109 ms  statement: SELECT "app_model_product"."id", "app_model_product"."title", "app_model_product"."category_id", "app_model_category"."id", "app_model_category"."name", "app_model_category"."is_active" FROM "app_model_product" INNER JOIN "app_model_category" ON ("app_model_product"."category_id" = "app_model_category"."id")
```

이제 다음과 같은 모델을 통해 `select_related`에 대한 내용을 좀 더 알아보자. 

```python
class City(models.Model):
    name = models.CharField(max_length=120)


class Person(models.Model):
    name = models.CharField(max_length=120)
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class Book(models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE)
```



그럼 반대로 `Category`모델에서 `Product`모델의 목록을 가져오는 경우에도 `select_related`를 통해 쿼리를 한번만 나가도록 수정할 수 있을까?   
우선 `category_list`함수를 `select_related`을 사용해서 다음과 같이 수정을 해보자. 

```python
@debugger_queries
def category_list_with_select_related():
    category = []
    # for product in Category.objects.select_related('product').first().product_set.all():
    for product in Category.objects.first().product_set.select_related('product').all():
        category.append({
            'id': product.id,
            'title': product.title,
            'category': product.category.name,
        })

    return category
```

위 함수를 실행시키면 `FieldError`가 발생한다. 

```python
FieldError: Invalid field name(s) given in select_related: 'product'. Choices are: category
```

함수를 다시 수정해서 주석을 서로 바꿔보자. 

```python
    for product in Category.objects.select_related('product').first().product_set.all():
    #for product in Category.objects.first().product_set.select_related('product').all():
```

이렇게 수정된 함수를 실행시키면, 역시 동일하게 `FieldError`가 발생한다. 

```python
FieldError: Invalid field name(s) given in select_related: 'product'. Choices are: (none)
```

# Reference

* [DjangoTip: Select & Prefetch Related](https://medium.com/@lucasmagnum/djangotip-select-prefetch-related-e76b683aa457)