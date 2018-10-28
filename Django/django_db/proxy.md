# [Proxy](https://docs.djangoproject.com/en/2.1/topics/db/models/#proxy-models)

```python
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class MyPerson(Person):
    class Meta:
        proxy = True
```

```sql
sqlite> .tables
app_model_article           auth_user
app_model_person            auth_user_groups
app_model_point             auth_user_user_permissions
app_model_userprofile       django_admin_log
auth_group                  django_content_type
auth_group_permissions      django_migrations
auth_permission             django_session
```
