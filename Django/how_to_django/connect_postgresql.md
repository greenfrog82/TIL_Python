# How to connect postgresql

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```


```sh
./manage.py migrate
Traceback (most recent call last):
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 20, in <module>
    import psycopg2 as Database
ModuleNotFoundError: No module named 'psycopg2'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "./manage.py", line 15, in <module>
    execute_from_command_line(sys.argv)
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
    utility.execute()
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/core/management/__init__.py", line 357, in execute
    django.setup()
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/__init__.py", line 24, in setup
    apps.populate(settings.INSTALLED_APPS)
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/apps/registry.py", line 112, in populate
    app_config.import_models()
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/apps/config.py", line 198, in import_models
    self.models_module = import_module(models_module_name)
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
  File "<frozen importlib._bootstrap>", line 983, in _find_and_load
  File "<frozen importlib._bootstrap>", line 967, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 677, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 728, in exec_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/contrib/auth/models.py", line 2, in <module>
    from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/contrib/auth/base_user.py", line 47, in <module>
    class AbstractBaseUser(models.Model):
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/models/base.py", line 101, in __new__
    new_class.add_to_class('_meta', Options(meta, app_label))
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/models/base.py", line 304, in add_to_class
    value.contribute_to_class(cls, name)
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/models/options.py", line 203, in contribute_to_class
    self.db_table = truncate_name(self.db_table, connection.ops.max_name_length())
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/__init__.py", line 33, in __getattr__
    return getattr(connections[DEFAULT_DB_ALIAS], item)
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/utils.py", line 202, in __getitem__
    backend = load_backend(db['ENGINE'])
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/utils.py", line 110, in load_backend
    return import_module('%s.base' % backend_name)
  File "/Users/greenfrog/.pyenv/versions/3.7.0/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/django/db/backends/postgresql/base.py", line 24, in <module>
    raise ImproperlyConfigured("Error loading psycopg2 module: %s" % e)
```

```sh
./manage.py migrate
/Users/greenfrog/.virtualenvs/django/lib/python3.7/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
  """)
Operations to perform:
  Apply all migrations: admin, app_model, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying app_model.0001_initial... OK
  Applying app_model.0002_person_try_to_travel... OK
  Applying app_model.0003_compareperson... OK
  Applying app_model.0004_auto_20181121_0313... OK
  Applying app_model.0005_auto_20181121_0316... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK
```