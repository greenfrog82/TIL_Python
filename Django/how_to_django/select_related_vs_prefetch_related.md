# select_related vs prefetch_related

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
for product in Product.objects.all(): # 여기서 쿼리가 한번 나간다. 
    products.append({
        'id': product.id,
        'title': product.title,
        'category': product.category.name, # 여기서 Product와 Category 테이블을 join하는 쿼리가 loop count 만큼 나간다. 
    })
...
```

실제로 실행된 쿼리의 로그를 보면 다음과 같다. 

```sql
[2019-03-03 13:22:44.822 UTC][277][5c7bd4f5.115][0]LOG:  duration: 2.567 ms  statement: SELECT "app_model_product"."id", "app_model_product"."title", "app_model_product"."category_id" FROM "app_model_product"
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

이와같이 ORM에서 루프를 돌기위한 쿼리가 1번 나가고 루프수만큼 N번 join 쿼리가나가는 문제는 **N+1 Query Problem**이라고 한다. 이는 성능에 심각한 영향을 끼치기 때문에 반드시 피해야한다. 

# Reference

* [DjangoTip: Select & Prefetch Related](https://medium.com/@lucasmagnum/djangotip-select-prefetch-related-e76b683aa457)