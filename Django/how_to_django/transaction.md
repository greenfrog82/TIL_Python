# Transaction

Django 1.4.22와 2.1 버전에서의 Transaction에 대한 내용을 정리한다.  

## [Transaction at Django 1.4.22](https://django.readthedocs.io/en/1.4.X/topics/db/transactions.html?highlight=autocommit#module-django.db.transaction)

### Django's default transaction behavior 

Django는 기본적으로 `auto commit`모드로 동작한다. `auto commit`모드란 Model객체의 `save()` 또는 `delete()`메소드를 호출할 때 변경사항을 즉시 `commit`하는것을 말한다. `auto commit`모드에서 `rollback`을 하는 방법은 없다.   

### Trying transactions to HTTP requests(request-based transaction)

HTTP request에서 트랜잭션을 다루는 추천되는 방법은 `request`와 `response` 사이클을 `django.middleware.transaction.TransactionMiddleware`을 통해 트랜잭션으로 묶는것이다.  
`TrasactionMiddleware`을 설정한 후 `request`가 `TrasactionMiddleware`을 통과하게 되면 트랜잭션이 시작된다. 그리고 `response`가 아무문제 없이 `TransactionMiddleware`을 통과했을때 `commit`을 하게되고, `exception`이 발생했다면 `rollback`하게 된다.   

위 동작을 실행시키기 위해서는 다음과 같이 `django.middleware.transaction.TransactionMiddleware`을 `settings.py`파일의 MIDDLEWARE_CLASSES에 추가해주면 된다.   

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)
```

이때 `TransactionMiddleware`를 적용하는 순서는 아주 중요한데, `TransactionMiddleware`는 `view` 뿐만 아니라 `middleware`에도 영향을 주기 때문이다. (이는 middleware가 request와 response를 처리하는 순서를 이해해야하는데  https://django.readthedocs.io/en/1.4.X/topics/http/middleware.html?highlight=middleware#activating-middleware을 참고하기 바란다.)

만약, `SessionMiddleware`를 다음과 같이 `TransactionMiddleware` 뒤에 위치시킨다면, session을 생성하는 부분은 트랙잭션의 `TransactionMiddleware`의 영향을 받는다.   

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)
```

`CacheMiddleware`, `UpdateCacheMiddleware` 그리고 `FetchFromCacheMiddleware`와 같이 다양한 `cache middleware`들은 `TransactionMiddleware`의 영향을 받지 않는다. 심지어 데이터베이스 캐쉬를 사용하고 있어도 영향을 받지 않는데, Django는 캐쉬를 위한 별도의 커서를 사용하기 때문이다. 

>**Note**
`TransactionMiddleware`는 DATABASES 설정의 'default'키로 설정 된 데이터베이스에 한하여 트랙잭션처리를 해준다. 따라서, 다른 데이터베이스에 트랙잭션을 처리해주고 싶다면 별도의 middleware를 개발해주어야한다.

### Controlling transaction management in Django Custom Command

정규문서에는 `View`를 통해 트랜잭션을 다루는 예들을 소개하고 있지만, 현재 Django Custom Command로 예제를 만드는것이 실습하기 편한것 같아서 여기서 Django Custom Command를 통해 관련 예들을 살펴본다.  

대부분의 경우 앞서 소개했던 `request-based transaction`을 통해 트랜잭션을 쉽게 다룰 수 있지만, `request` 전체에 트랜잭션을 걸기 때문에 성능상 손해를 많이 보게된다. 따라서 세밀하게 트랜잭션을 다뤄줘야할 필요가 있는데 이러한 경우 `django.db.transaction`클래스를 통해 `per-function` 또는 `per-code-block` 기준으로 트랜잭션을 다룰 수 있다.  

#### Per-Function

함수 레벨의 트랜잭션은 `decorator`를 통해 처리할 수 있다.  
다음 코드의 경우 함수의 호출이 정상적으로 이루어진 경우 `commit`이 이루어지고 exception이 발생한 경우 `rollback`된다.  

```python
from django.db import transaction

@transaction.commit_on_success
def viewfunc(request):
    # ...
    # this code executes inside a transaction
    # ...
```

#### Per-Code-Block

코드 블록 레벨의 트랜잭션은 `context manager`를 통해 처리 할 수 있다. 
다음 코드의 경우 `context manager`로 감싸진 부분은 정상적으로 코드가 실행 되면 `commit`이 이루어지고 exception이 발생한 경우 `rollback`된다. 그리고 `context manager`이외의 코드에서는 Django의 기본 트랜잭션 처리(AUTOCOMMIT)가 이루어진다. 

```python
from django.db import transaction

def viewfunc(request):
    # ...
    # this code executes using default transaction management
    # ...

    with transaction.commit_on_success():
        # ...
        # this code executes inside a transaction
        # ...
```

#### How to check that current transaction is managed or not.

`django.db.transaction`모듈에는 `is_managed()`라는 함수가 있다. 이 함수를 통해 해당 트랜잭션이 `AUTOCOMMIT`모드 동작 중인지 아니면 개발자가 `commit_on_success`나 `commit_manually`를 통해 열어놓은것인지 확인할 수 있다.   
해당 함수는 다음과 같이 구현되어있다. 

```python
def is_managed(using=None):
    """
    Checks whether the transaction manager is in manual or in auto state.
    """
    if using is None:
        using = DEFAULT_DB_ALIAS
    connection = connections[using]
    return connection.is_managed()

# django.db.backends 모듈의 BaseDatabaseWrapper의 함수로 django.db.transaction.is_managed 함수가 내부적으로 호출하는 connection.is_managed()이다.
def is_managed(self):
        """
        Checks whether the transaction manager is in manual or in auto state.
        """
        if self.transaction_state:
            return self.transaction_state[-1]
        return settings.TRANSACTIONS_MANAGED
```

`is_managed()`함수의 리턴값의 의미는 다음과 같다.

* **True** : 현재 트랜잭션은 `commit_on_success`나 `commit_manually`을 통해 열린것이다. 
* **False** : 현재 트랜잭션은 `AUTOCOMMIT`모드로 동작 중이다.

그러면 `Per-Code-Block`으로 트랜잭션을 관리할 때 현재 실행되고 있는 코드의 트랜잭션이 어떤 상태로 관리되고 있는지 확인해보자. 

**commit_on_success 일 때**

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Is AUTOCOMMIT Mode managed? {}\n'.format(transaction.is_managed()))

        with transaction.commit_on_success():
            self.stdout.write('Is commit_on_successs managed? {}\n'.format(transaction.is_managed()))
```

출력결과를 보면 다음과 같다. 

```
Is AUTOCOMMIT Mode managed? False
Is commit_on_successs managed? True
```

**commit_manually 일 때**

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Is AUTOCOMMIT Mode managed? {}\n'.format(transaction.is_managed()))

        with transaction.commit_manually():
            self.stdout.write('Is commit_manually managed? {}\n'.format(transaction.is_managed()))
```

출력결과를 보면, 앞서 `commit_on_success`와 동일함을 알 수 있다.

```
Is AUTOCOMMIT Mode managed? False
Is commit_on_successs managed? True
```

**autocommit 일 때**

앞서 테스트 결과들을 보면 `commit_on_success`와 `commit_manually`를 사용해 트랜잭션을 연 경우와 Django의 기본 트랜잭션(AUTOCOMMIT)을 사용했을 때 결과가 달리나왔다. 그렇다면 `autocommit`을 사용하면 어떻게 될까? 예상을 해보면 `autocommit`을 Django의 기본 트랜잭션 모드의 설정에 관계없이 AUTOCOMMIT 모드를 보장하기 위한 것이기 때문에 `is_managed()`함수의 호출 결과가 `False`가 나와야한다. 확인해보자. 

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Is AUTOCOMMIT Mode managed? {}\n'.format(transaction.is_managed()))

        with transaction.autocommit():
            self.stdout.write('Is autocommit managed? {}\n'.format(transaction.is_managed()))
```

결과는 예상과 같다. 

```
Is AUTOCOMMIT Mode managed? False
Is autocommit managed? False
```

위 결과를 보면 다음과 같다. 

* **is_managed()가 True인 경우**는 `commit_on_success`와 `commit_manually`와 같이 INSERT/UPDATE/DELETE 쿼리가 발생헀을 때 바로 `COMMIT`을 수행하지 않고 명시적 또는 암시적 `COMMIT`수행을 해야하고 `ROLLBACK`이 가능한 트랜잭션이다. 
* **is_managed()가 False인 경우**는 `AUTOCOMMIT`모드로 INSERT?UPDATE/DELETE 쿼리 발생 시 바로 `COMMIT`을 수행하고 명시적 또는 암시적 `ROLLBACK`이 불가능한 트랜잭션이다. 

>**Noete**
Django에서 트랜잭션을 다루기 위한 `per-function`과 `per-code-block`방식의 `view`, `function`, `method` 어디에서든 사용가능하다.

Django가 지원하는 각각의 트랜잭션 방법을 알아보기 전에 에제를 만들기 위해 다음과 같은 모델을 정의하자.  

```python
class Person(models.Model):
    name = models.CharField(max_length=120)
```

#### autocommit

`autocommit`decorator는 Django의 전역 트랜잭션 설정이 어떻든간에 Django의 `auto-commit`을 수행한다.  
따라서 `save()`, `delete()`등과 같이 `쓰기`동작을 수행하는 경우 즉시 `commit`이 이루어진다.   

다음과 같은 `command`를 정의하고 호출해보자.

```python
class Command(BaseCommand):
    @transaction.autocommit
    def handle(self, *args, **options):
        Person.objects.create(name='test')
```

호출 후 Django Shell에서 데이터를 확인해보면 방금 입력한 데이터가 저장된 것을 확인할 수 있다. (테스트를 위해 `Person`을 비워놨다.)

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'test'
```

이번에는 즉시 `commit`이 되는것이 맞는지 확인하기 위해서 `transaction.rollback`을 호출해보자.  

```python
class Command(BaseCommand):
    @transaction.autocommit
    def handle(self, *args, **options):
        Person.objects.create(name='test-rollback')
        transaction.rollback()
```

결과를 확인해보면 모델을 생성하고 저장하는 즉시 `commit`되었기 때문에 `rollback`이 되지 않는것을 확인할 수 있다.  

```python
>>> Person.objects.all()
[<Person: Person object>, <Person: Person object>]
>>> Person.objects.all()[1].name
u'test_rollback'
>>>
```

#### commit_on_success

다음 코드의 경우 함수의 호출이 정상적으로 이루어진 경우 `commit`이 이루어지고 exception이 발생한 경우 `rollback`된다.  

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='commit_on_success')
```

결과를 보면 함수 호출의 문제가 없었으므로 정상적으로 `commit`이 된것을 확인 할 수 있다.   

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'commit_on_success'
>>>
```

이번에는 예외를 발생시켜서 `rollback`이 이루어지는지 확인해보자.   

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='raise exception on commit_on_success')
        raise Exception('test commit_on_success')
```

실행 결과를 확인해보면 다음과 같이 `rollback`이 이루어져 이전에 `commit`헀던 결과만이 출력됨을 알 수 있다. 

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'commit_on_success'
```

혹시나해서 다음과 같이 `transaction.rollback`을 호출해 보았다. 

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='commit_on_success with transaction.rollback')
        transaction.rollback()
```

이 경우 다음과 같이 `rollback`이 이루어진다.

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'commit_on_success'
>>>
```

#### commit_manually

앞서 다뤘던 방법들과 달리 모든 트랜잭션을 개발자가 직접 다뤄줘야한다.  
만약 DB가 변경되는 행위를 했는데 (ex. save(), delete() 호출 시) `commit` 또는 `rollback`을 호출하지 않으면, `TransactionManagementError` exception이 발생한다.  

앞서 테스트했던 데이터들을 지우고 다음 코드를 실행해보자.   

```python
class Command(BaseCommand):
    @transaction.commit_manually
    def handle(self, *args, **options):
        Person.objects.create(name='transaction.commit_manually')
```

명시적으로 `commit`또는 `rollback`을 하고있지 않기 때문에 `TransactionManagementError`가 발생한다.   

```bash
 in leave_transaction_management
    raise TransactionManagementError("Transaction managed block ended with "
django.db.transaction.TransactionManagementError: Transaction managed block ended with pending COMMIT/ROLLBACK
```

`TransactionManagementError`가 발생하면 다음과 같이 데이터가 `commit`되지 않는다.  

```python
>>> Person.objects.all()
[]
```

이번에는 위 에제에서 `commit` 함수를 호출해보자.  
여기서 주의할 점은 `commit_manually`를 사용하는 동안은 모든 `commit`과 `rollback`을 개발자가 해주어야하기 때문에 `try-raise-else`를 통해 `commit`과 `rollback`을 제어해주어야한다.  
앞선 예제에서는 `TransactionManagementError`의 발생을 확인하기 위해서 `try-raise-else`를 생략했었다.  

```python
class Command(BaseCommand):
    @transaction.commit_manually
    def handle(self, *args, **options):
        try:
            Person.objects.create(name='transaction.commit_manyally')
        raise Exception as e:
            transaction.rollback()
        else:
            transaction.commit()
```

정상적으로 `commit`이 이루어졌음을 알 수 있다.  

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'transaction.commit_manually'
>>>
```

이번에는 loop를 돌려 첫번째, 두번째 객체는 `commit`하고 마지막 세번째 객체는 `rollback`해보자. 

```python
class Command(BaseCommand):
    @transaction.commit_manually
    def handle(self, *args, **options):
        for i in xrange(1, 4):
            try:
                if 3 > i:
                    Person.objects.create(name=str(i))
                else:
                    raise Exception('rollback test')
            except:
                transaction.rollback()
            else:
                transaction.commit()
```

실행 결과를 보면 첫번째와 두번째 객체는 `commit`을 수행하였으므로 데이터가 저장되었지만 세번째 객체는 `rollback`되어 데이터가 존재하지 않음을 알 수 있다. 

```python
>>> Person.objects.all()
[<Person: Person object>, <Person: Person object>]
>>> Person.objects.all()[0].name
u'1'
>>> Person.objects.all()[1].name
u'2'
```

## Requirements for transaction handling

앞선 예제에서 알아 본 것과 같이 트랜잭션은 요청이 끝나기 전에 열기고 닫혀야한다. `autocommit`이나 `commit_on_success`를 사용하는 경우 자동적으로 처리가 된다.   
하지만 `commit_manually`를 사용하고 있는 경우는 개발자가 요청이 끝나기 전에 `commit` 또는 `rollback`을 반드시 호출해주어야한다.  

이미 이와 같은 내용을 언급했음에도 불구하고 다시 강조하는 이유는 `save()`, `delete()`와 같은 `쓰기`작업 이외에도 `읽기`작업에도 동일하게 이루어져야하기 때문이다.

다음 코드를 보자.
`commit_manually`를 사용하고 있고 `읽기`작업만 수행하고 있다. 그리고 `commit`또는 `rollback`을 호출하고 있지 않다.   
이때 `list()`을 통해 `QuerySet`을 evaluation했는데, **`QuerySet`을 Lazy Evaluation을 하기 때문에 evaluation해주지 않으면 DB connection이 일어나지 않고 트랜잭션이 열리지 않기 때문이다.** 

```python
class Command(BaseCommand):
    @transaction.commit_manually
    def handle(self, *args, **options):
        qs = Person.objects.all()
        arr = list(qs.values_list())
```

실행 결과는 다음과 같다.

```bash
 in leave_transaction_management
    raise TransactionManagementError("Transaction managed block ended with "
django.db.transaction.TransactionManagementError: Transaction managed block ended with pending COMMIT/ROLLBACK
```

앞서 설명한 것과 같이 `TransactionManageError`를 발생시키지 않기 위해서는 `commit`또는 `rollback`을 명시적으로 호출해서 트랜잭션을 닫아주어야한다.   

```python
class Command(BaseCommand):
    @transaction.commit_manually
    def handle(self, *args, **options):
        try:
            qs = Person.objects.all()
            arr = list(qs.values_list())
        raise:
            transaction.rollback()
        else:
            transaction.commit()
```

### commit_on_success vs commit_manually

사실 `commit_on_success`의 코드를 보면 다음과 같은데, context manager로 코드가 진입할 때 트랜잭션을 열고 context manager를 코드가 빠져나갈때 INSERT/UPDATE/DELETE 쿼리 존재여부를 확인해서 자동으로 `COMMIT`을 실행하거나 `ROLLBACK`을 해주는 역할을 해줄 뿐이지 `commit_manually`의 구현체와 동일하다. 또한 코드 내부에서 호출되고 있는 `rollback`, `commit`함수들은 `django.db.transaction`모듈에 있는 것들이다.   

```python
def commit_on_success(using=None):
    """
    This decorator activates commit on response. This way, if the view function
    runs successfully, a commit is made; if the viewfunc produces an exception,
    a rollback is made. This is one of the most common ways to do transaction
    control in Web apps.
    """
    def entering(using):
        enter_transaction_management(using=using)
        managed(True, using=using)

    def exiting(exc_value, using):
        try:
            if exc_value is not None:
                if is_dirty(using=using):
                    rollback(using=using)
            else:
                if is_dirty(using=using):
                    try:
                        commit(using=using)
                    except:
                        rollback(using=using)
                        raise
        finally:
            leave_transaction_management(using=using)

    return _transaction_func(entering, exiting, using)

def commit_manually(using=None):
    """
    Decorator that activates manual transaction control. It just disables
    automatic transaction control and doesn't do any commit/rollback of its
    own -- it's up to the user to call the commit and rollback functions
    themselves.
    """
    def entering(using):
        enter_transaction_management(using=using)
        managed(True, using=using)

    def exiting(exc_value, using):
        leave_transaction_management(using=using)

    return _transaction_func(entering, exiting, using)
```

무슨말이 하고 싶은거냐면, 데이터베이스의 트랜잭션이 `commit_on_success`용 따로 `commit_manually`용이 따로 있는것이 아니기 때문에 결국 `Managed Transaction`을 사용하는 두 함수들내부에서는 얼마든지 `django.db.transaction`모듈의 `rollback`과 `commit`함수를 얼마든지 사용할 수 있다. 사실 처음에 두 함수들을 공부했을 때 `rollback`과 `commit`함수는 `commit_manually`에서만 사용하는 줄 알았다.  

다만 앞서 `commit_on_success`의 구현을 보면 알곘지만, `rollback`과 `commit`을 암시적으로하고 있기 때문에 명시적으로 이들의 호출이 필요한 경우가 아니라면 굳이 호출해 줄 필요가 없고 그런 경우라면 차라리 `commit_manually`를 사용하는것이 혼란이 없을 것 같다. 

이쯤에서 하나 궁금해지는건 `commit_on_success`는 `rollback`과 `commit`을 수행하기 위해 별도의 검사를 수행하기 때문에 개발자가 직접 `rollback`과 `commit`을 수행하는 `commit_manually`보다 미세하게 나마 성능에 차이가 있지 않을까? 확인해보자. 

```python
import time

from django.core.management.base import BaseCommand
from django.db import transaction
from dowant.test_transaction.models import Person

# 1. commit_on_success
class Command(BaseCommand):
    def handle(self, *args, **options):
        begin = time.time()
        exec_cnt = 100

        for idx in range(exec_cnt):
            with transaction.commit_on_success():
                Person.objects.create(name='commit_on_success_{}'.format(idx))

        self.stdout.write('--- {} seconds\n'.format((time.time() - begin) / exec_cnt))

# 2. commit_manually
class Command(BaseCommand):
    def handle(self, *args, **options):
        begin = time.time()
        exec_cnt = 100

        for idx in range(exec_cnt):
            with transaction.commit_manually():
                Person.objects.create(name='commit_manually_{}'.format(idx))
                transaction.commit()

        self.stdout.write('--- {} seconds\n'.format((time.time() - begin) / exec_cnt))
```

각각 두 Django Custom Command의 실행 결과는 다음과 같고, 별 차이가 없다. 

```
# 1. commit_on_success
--- 0.000612988471985 seconds%                                                            
# 2. commit_manually
--- 0.000596458911896 seconds
```

## SavePoints

`SavePoints`는 트랜잭셔 내부에서 부분적으로 트랜잭션을 다루기 위한 것이다. PostgreSQL 8, Oracle, MySQL(ver 5.0.3 이상, InnoDB Engine)가 이를 지원하며, 지원하지 않는 DB를 사용하는 경우 해당 기능은 동작하지 않는다.

`SavePoints`는 `autocommit`의 경우 모든 동작을 즉시 `commit` 해버리기 때문에 사용할 수 없다.   
`SavePoints`는 `commit_on_success`와 `commit_manually`를 사용할 때 유용하며 부분적인 트랜잭션을 수행할 수 있다. 

`SavePoints`는 다음 세가지 메소드를 통해 제어된다. 

>transaction.savepoint(using=None)

`savepoint`를 생성하며 `savepoint ID(sid)`를 반환한다. 이 반환된 `sid`를 통해 해당 `savepoint`에 대한 `commit`과 `rollback`이 이루어진다.   

>transaction.savepoint_commit(sid, using=None)

인자로 전달받은 `sid`가 포함하고 있는 DB operation을 `commit`한다.

>transaction.savepoint_rollback(sid, using=None)

인자로 전달받은 `sid`가 포함하고 있는 DB operation을 `rollback`한다. 

### Example

앞서 `autocommit`모드에서는 `Savepoints`의 동작이 무의미하다고 언급했었다. 
정말 그런지 확인해보자.

```python
class Command(BaseCommand):
    @transaction.autocommit
    def handle(self, *args, **options):
        sid = transaction.savepoint()
        Person.objects.create(name='test')
        transaction.savepoint_rollback(sid)
```

앞선 에제에서 `SavePoints`에 대해서 `rollback`을 했지만, `commit`이되어 데이터가 존재하는 것을 확인 할 수 있다. 

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'test'
>>>
```

이번에는 `commit_on_success`에서 `SavePoints`를 테스트해보자.  
우선, `SavePoints`를 `commit`하지 않으면 어떻게 될까? 객체를 생성한 후 `commit`을 생략해보자.  

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        sid = transaction.savepoint()
        Person.objects.create(name='test commit_on_success without savepoint_commit')
```

`commit_on_success`는 해당 함수의 동작이 정상적으로 호출되면 `commit`을 수행하므로 해당 데이터가 저장된 것을 확인 할 수 있다. 

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'test commit_on_success without savepoint_commit'
>>>
```

이번에는 `SavePoints` 바깥 트랜잭션에서 데이터를 하나 생성하고, `SavePoints` 안쪽에서 생성한 데이터를  `savepoint_rollback`을 통해서 `rollback`해보자. 

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='commit_on_success')
        
        sid = transaction.savepoint()
        Person.objects.create(name='test commit_on_success without savepoint_commit')
        transaction.savepoint_rollback(sid)
```

실행결과를 보면 `SavePoints`의 데이터는 `rollback`된 것을 확인할 수 있다. 

```python
>>> Person.objects.all()
[<Person: Person object>]
>>> Person.objects.all()[0].name
u'commit_on_success'
>>>
```

`SavePoints`의 바깥 트랜잭션은 `rollback`을 하고, `SavePoints` 안쪽에서 생성한 데이터를 `commit`하면 어떻게 될까?

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='commit_on_success')
        
        sid = transaction.savepoint()
        Person.objects.create(name='test commit_on_success without savepoint_commit')
        transaction.savepoint_commit(sid)

        raise Exception('commit_on_success raise exception')
```

위 예제를 실행하면 다음과 같이 exception이 발생한다. 앞서 설명한것과 같이 `commit_on_success`는 exception이 발생하면 해당 트랜잭션을 `rollback`시킨다.

```bash
    raise Exception('commit_on_success raise exception')
Exception: commit_on_success raise exception
```

Djagno Shell에서 데이터를 확인해보면 `SavePoints`는 `commit`을 했지만 바깥쪽 트랜잭션이 `rollback`되면 함께 데이터가 `rollback`되는 것을 확인 할 수 있다.  

```python
>>> Person.objects.all()
[]
```

>이 부분이 아주 중요한데, `SavePoints`를 `commit`했다 하더라도 실제적인 `commit`은 바깥쪽 트랜잭션에 영향을 받는다. 바깥쪽 트랜잭션에서 `commit`을 해주지 않으며 `SavePoints`의 `commit`이 이루어지지 않는다.  
만약 바깥쪽 트랜잭션에서 `rollback`을 해버린다면 `SavePoints`의 `commit` 역시 모두 `rollback`되어 버린다.

이러한 특징은 `commit_manually`를 통해 좀 더 직관적으로 이해할 수 있다. 다음과 같은 예제를 작성해보자.

1. 바깥쪽 트랜잭션에서는 `commit`을 수행하고 `SavePoints`에서도 `commit`을 호출한다.  
2. 바깥쪽 트랜잭션에서는 `commit`을 수행하고 `SavePoints`에서는 `rollback`을 호출한다.  
3. 바깥쪽 트랜잭션에서는 `rollback`을 수행하고 `SavePoints`에서는 `commit`을 호출한다.

```python
class Command(BaseCommand):
    @transaction.commit_manually
    def handle(self, *args, **options):
        Person.objects.create(name='First Transaction')

        sid = transaction.savepoint()
        Person.objects.create(name='First SavePoints')
        transaction.savepoint_commit(sid)

        transaction.commit()

        Person.objects.create(name='Second Transaction')

        sid = transaction.savepoint()
        Person.objects.create(name='Second SavePoints')
        transaction.savepoint_rollback(sid)

        transaction.commit()

        Person.objects.create(name='Third Transaction')

        sid = transaction.savepoint()
        Person.objects.create(name='Third SavePoints')
        transaction.savepoint_commit(sid)

        transaction.rollback()
```

실행결과를 보면 첫번째 트랜잭션 결과는 `commit`되었고 두번째 트랜잭션은 `rollback`되었으며, 마지막 세번째 트랜잭션은 바깥쪽 트랜잭션은 `commit`되고 안쪽 트랜잭션은 `rollback`된 것을 확인 할 수 있다.

```python
In [3]: [person.name for person in Person.objects.all()]
Out[3]: [u'First Transaction', u'First SavePoints', u'Second Transaction']
```

## When do we use SavePoints?

개발자는 다음과 같은 의도로 다음 예제를 개발하였다.  

1. 'A'를 생성한다.
2. 'B'를 생성할 때 Exception이 발생하면 'B'데이터 생성에 대해서만 `rollback`을 한다.
3. 'C'를 생성한다.

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='A')

        try:
            Person.objects.create(name='B')
            raise Exception
        except:
            transaction.rollback()

        Person.objects.create(name='C')
```

실행결과는 다음과 같이 의도치 않게 데이터 'A'까지 `rollback`되어 버렸다.   

```python
In [7]: [person.name for person in Person.objects.all()]
Out[7]: [u'C']
```

이러한 경우, `SavePoints`를 사용하면 이 문제를 쉽게 해결할 수 있다.  

```python
class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        Person.objects.create(name='A')

        sid = transaction.savepoints()
        try:
            Person.objects.create(name='B')
            raise Exception
        except:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

        Person.objects.create(name='C')
```


```python
In [10]: [person.name for person in Person.objects.all()]
Out[10]: [u'A', u'C']
```

## Database-level autocommit

PostgreSQL 8.2 이상 버전을 사용하면 `database-level autocommit` 옵션을 사용할 수 있다. 만약, 이 옵션을 사용하면 항상 열려있는 트랜잭션이 없기 때문에 exception이 처리 된 후에도 작업을 계속할 수 있다. 

```python
a.save() # succeeds
try:
    b.save() # Could throw exception
except IntegrityError:
    pass
c.save() # succeeds
```

>**Note**
`database-level autocommit`은 `autocommit decorator`와 동작이 비슷해 보이지만 엄연히 다르다. `database-level autocommit`은 계속적인 트랜잭션이 존재하지 않지만, `autocommit decorator`는 각각 동작을 수행할 때 트랜잭션이 존재하며 DB가 수정될 때 `commit`이 발생한다.  

### TODO

* Database-level autocommit 시 `commit_on_success`와 `commit_manually`등에 미치는 영향과 이점과 허점등을 조사해볼 것. 우선순위 최하!!