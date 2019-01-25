# [Managers](https://docs.djangoproject.com/en/2.1/topics/db/managers/#managers)


## [Calling custom QuerySet methods from the manager](https://docs.djangoproject.com/en/2.1/topics/db/managers/#calling-custom-queryset-methods-from-the-manager)

표준 QuerySet이 제공하는 메소드들은 Manager를 통해 직접 접근이 가능하지만, Custom QuerySet에 추가적인 메소드가 정의된 경우 이를 사용하기 위해서는 Manager에 이를 사용하기 위한 메소드를 정의해주어야한다.

```python
class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role='A')

    def editors(self):
        return self.filter(role='E')

class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def authors(self):
        return self.get_queryset().authors()

    def editors(self):
        return self.get_queryset().editors()

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=(('A', _('Author')), ('E', _('Editor'))))
    people = PersonManager()
```