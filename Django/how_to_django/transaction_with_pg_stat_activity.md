# Django ORM and Transaction

## Auto Commit Mode

### Select Only 

```python
def tx_autocommit(request):
    user = User.objects.latest('pk')
    import ipdb; ipdb.set_trace()
    pk = user.pk

    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

pgsql의 로그를 보면 첫번째 브레이크 포인트에서 다음과 같이 트랜잭션을 열고 쿼리를 날리는것으 알 수 있다. 

```
[2019-02-22 08:01:23.308 KST][88956][5c6f2dc3.15b7c][0]LOG:  duration: 0.705 ms  statement: SHOW default_transaction_isolation
[2019-02-22 08:01:23.311 KST][88956][5c6f2dc3.15b7c][0]LOG:  duration: 2.897 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-02-22 08:01:23.312 KST][88956][5c6f2dc3.15b7c][0]LOG:  duration: 0.040 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:01:23.316 KST][88956][5c6f2dc3.15b7c][0]LOG:  duration: 4.195 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" ORDER BY "auth_user"."id" DESC LIMIT 1`
```

이때 pg_stat_activity 테이블을 통해 디비의 상태를 확인하면 `trasaction in idle` 상태인것을 알 수 있다. 

```
datid | datname |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                                   query
-------+---------+-------+----------+------+---------+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | greenfrog   | 81912 | postgres | psql | f       | active              | select datid, datname, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | greenfrog | 88956 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" ORDER BY "auth_user"."id" DESC LIMIT 1
(2 rows)
```

이제 해당 요청을 처리해보자. 그러면 pgsql의 로그을 통해 다음과 같이 `COMMIT`을 하고 있음을 알 수 있다. 

```
[2019-02-22 08:05:37.990 KST][88956][5c6f2dc3.15b7c][0]LOG:  duration: 0.033 ms  statement: COMMIT
```

이떄 pg_stat_activity 테이블을 통해 디비의 상태를 확인해보면 해당 요청에 대한 세션(88956)이 끊어졌음을 알 수 있다.

```
select datid, datname, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 datid | datname |  pid  | usename  | app  | waiting | state  |                                                    query
-------+---------+-------+----------+------+---------+--------+-------------------------------------------------------------------------------------------------------------
 16392 | greenfrog | 81912 | postgres | psql | f       | active | select datid, datname, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
(2 rows)
```

### Select and Insert, Update and Delete

앞서 살펴본바와 같이 Django는 `Autocommit`모드에서 트랜잭션을 연 후 요청이 끝나면 `COMMIT`을 수행한다. 그렇다면 **Insert, Update, Delete** Operation이 있을때는 어떻게 동작하게 될까?

#### Select and Insert

```python
def tx_autocommit(request):
    user = User.objects.latest('pk')
    import ipdb; ipdb.set_trace()
    user = User.objects.create(username='tx_test_a')
    ipdb.set_trace()
    
    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

**break point 1.**

위를 실행하면 앞서와 같이 첫번쨰 브레이크 포인트에서 디비 연결을 하고 트랜잭션을 연 후 쿼리를 날리고 있음을 알 수 있다. 

```
[2019-02-22 08:16:07.836 KST][90834][5c6f3137.162d2][0]LOG:  duration: 0.150 ms  statement: SHOW default_transaction_isolation
[2019-02-22 08:16:07.836 KST][90834][5c6f3137.162d2][0]LOG:  duration: 0.391 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-02-22 08:16:07.837 KST][90834][5c6f3137.162d2][0]LOG:  duration: 0.035 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:16:07.839 KST][90834][5c6f3137.162d2][0]LOG:  duration: 1.924 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" ORDER BY "auth_user"."id" DESC LIMIT 1
[2019-02-22 08:16:12.132 KST][81912][5c6ed233.13ff8][0]LOG:  duration: 0.496 ms  statement: select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
```

역시 디비의 상태는 `transaction in idle`이다. 

```
datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                                   query
-------+-------+----------+------+---------+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 90834 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" ORDER BY "auth_user"."id" DESC LIMIT 1
 ```

**break point 2.**

 이제 다음 브레이크 포인트로 이동해서 사용자를 생성하고 저장해보자. 
 데이터 insert 쿼리를 날린 후 `COMMIT`을 하고 다시 트랜잭션을 연 후 `customer_userleavinginfo`테이블을 select한 후 다시 `COMMIT`을 하고 있음을 알 수 있다.

 ```
[2019-02-22 08:18:14.399 KST][90834][5c6f3137.162d2][305872]LOG:  duration: 11.559 ms  statement: INSERT INTO "auth_user" ("username", "first_name", "last_name", "email", "password", "is_staff", "is_active", "is_superuser", "last_login", "date_joined") VALUES ('tx_test_a', '', '', '', '', false, true, false, '2019-02-22 08:18:14.386068', '2019-02-22 08:18:14.386101') RETURNING "auth_user"."id"
[2019-02-22 08:18:14.401 KST][90834][5c6f3137.162d2][0]LOG:  duration: 0.763 ms  statement: COMMIT
[2019-02-22 08:18:14.422 KST][90834][5c6f3137.162d2][0]LOG:  duration: 0.036 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:18:14.428 KST][90834][5c6f3137.162d2][0]LOG:  duration: 5.844 ms  statement: SELECT "customer_userleavinginfo"."user_id", "customer_userleavinginfo"."is_deleted", "customer_userleavinginfo"."left_at", "customer_userleavinginfo"."reason", "customer_userleavinginfo"."is_dormant_user" FROM "customer_userleavinginfo" WHERE "customer_userleavinginfo"."user_id" = 147993
[2019-02-22 08:18:14.431 KST][90834][5c6f3137.162d2][0]LOG:  duration: 0.027 ms  statement: COMMIT
```

디비 상태는 `COMMIT`을 했으므로 `idle`상태이다.

```
 datid |  pid  | usename  | app  | waiting | state  |                                               query
-------+-------+----------+------+---------+--------+----------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 90834 | postgres |      | f       | idle   | COMMIT
 ```


#### Update and Select


```python
def tx_autocommit(request):
    User.objects.filter(username='tx_test_a').update(username='tx_test_update')
    import ipdb; ipdb.set_trace()
    users = User.objects.filter(username='tx_test_update')
    ipdb.set_trace()
    for user in users:
        print user
        
    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

**break point 1.**

```
[2019-02-22 08:24:08.055 KST][91509][5c6f3318.16575][0]LOG:  duration: 0.165 ms  statement: SHOW default_transaction_isolation
[2019-02-22 08:24:08.056 KST][91509][5c6f3318.16575][0]LOG:  duration: 0.438 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-02-22 08:24:08.056 KST][91509][5c6f3318.16575][0]LOG:  duration: 0.034 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:24:08.062 KST][91509][5c6f3318.16575][305873]LOG:  duration: 6.306 ms  statement: UPDATE "auth_user" SET "username" = 'tx_test_update' WHERE "auth_user"."username" = 'tx_test_a'
[2019-02-22 08:24:08.068 KST][91509][5c6f3318.16575][0]LOG:  duration: 0.277 ms  statement: COMMIT
```

```
 datid |  pid  | usename  | app  | waiting | state  |                                               query
-------+-------+----------+------+---------+--------+----------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 90834 | postgres |      | f       | idle   | COMMIT
 ```

**break point 2.**

```
[2019-02-22 08:26:12.200 KST][91509][5c6f3318.16575][0]LOG:  duration: 0.036 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:26:12.201 KST][91509][5c6f3318.16575][0]LOG:  duration: 0.320 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'tx_test_update'
```

```
 datid |  pid  | usename  | app  | waiting | state  |                                               query
-------+-------+----------+------+---------+--------+----------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 91509 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'tx_test_update'2.***
```

## Commit Manually

### Only using commit_manually

```python
def tx_commit_manually(request):
    with transaction.commit_manually():
        user = User.objects.get(username='tx_test_update')
        import ipdb; ipdb.set_trace()

        user.username = 'tx_test_save'
        user.save()
        ipdb.set_trace()

        transaction.commit()
        ipdb.set_trace()
```

**break point 1.**

```
[2019-02-22 08:40:09.384 KST][92889][5c6f36d9.16ad9][0]LOG:  duration: 0.182 ms  statement: SHOW default_transaction_isolation
[2019-02-22 08:40:09.385 KST][92889][5c6f36d9.16ad9][0]LOG:  duration: 0.489 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-02-22 08:40:09.385 KST][92889][5c6f36d9.16ad9][0]LOG:  duration: 0.066 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:40:09.388 KST][92889][5c6f36d9.16ad9][0]LOG:  duration: 2.840 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'tx_test_update'
```

```
 datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                                        query
-------+-------+----------+------+---------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 92889 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'tx_test_update'
 ```

**break point 2.**

`save()`함수를 호출했음에도 불구하고 `autocommit`모드와 달리 `COMMIT`이 호출되지 않았다. 

```
[2019-02-22 08:41:36.374 KST][92889][5c6f36d9.16ad9][0]LOG:  duration: 1.067 ms  statement: SELECT (1) AS "a" FROM "auth_user" WHERE "auth_user"."id" = 147993  LIMIT 1
[2019-02-22 08:41:36.379 KST][92889][5c6f36d9.16ad9][305874]LOG:  duration: 1.095 ms  statement: UPDATE "auth_user" SET "username" = 'tx_test_save', "first_name" = '', "last_name" = '', "email" = '', "password" = '', "is_staff" = false, "is_active" = true, "is_superuser" = false, "last_login" = '2019-02-22 08:18:14.386068', "date_joined" = '2019-02-22 08:18:14.386101' WHERE "auth_user"."id" = 147993
[2019-02-22 08:41:36.398 KST][92889][5c6f36d9.16ad9][305874]LOG:  duration: 0.600 ms  statement: SELECT "customer_userleavinginfo"."user_id", "customer_userleavinginfo"."is_deleted", "customer_userleavinginfo"."left_at", "customer_userleavinginfo"."reason", "customer_userleavinginfo"."is_dormant_user" FROM "customer_userleavinginfo" WHERE "customer_userleavinginfo"."user_id" = 147993
```

여전히 `transaction in idle`

```
 datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                               query
-------+-------+----------+------+---------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 92889 | postgres |      | f       | idle in transaction | SELECT "customer_userleavinginfo"."user_id", "customer_userleavinginfo"."is_deleted", "customer_userleavinginfo"."left_at", "customer_userleavinginfo"."reason", "customer_userleavinginfo"."is_dormant_user" FROM "customer_userleavinginfo" WHERE "customer_userleavinginfo"."user_id" = 147993
 ``` 

**break point 3.**

`transaction.commit()`함수 호출과 동시에 `COMMIT`이 되었음을 알 수 있다. 
```
[2019-02-22 08:44:14.075 KST][92889][5c6f36d9.16ad9][0]LOG:  duration: 0.763 ms  statement: COMMIT
```

`COMMIT`되었으니 `idle`상태로 변경되었다. 

```
 datid |  pid  | usename  | app  | waiting | state  |                                               query
-------+-------+----------+------+---------+--------+----------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 92889 | postgres |      | f       | idle   | COMMIT
```

이미 `COMMIT`을 하였으니 `autocommit`모드와 달리 요청을 끝내도 `COMMIT`이 호출되지 않는다.  

### Doing query after commit with commit_manually

`commit_manually`를 사용할때 `commit`을 수행한 후 다시 쿼리를 수행하면 어떻게 될까?

```python
@transaction.commit_manually
def tx_commit_manually(request):
    user = User.objects.get(username='tx_test_update')
    import ipdb; ipdb.set_trace()
    transaction.commit()

    user = User.objects.all()[0]
    ipdb.set_trace()
    transaction.commit()
```

**break point 1.**

```
[2019-02-22 09:13:22.047 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 0.170 ms  statement: SHOW default_transaction_isolation
[2019-02-22 09:13:22.048 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 0.697 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-02-22 09:13:22.048 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 0.070 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 09:13:22.050 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 2.139 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" LIMIT 1 OFFSET 1
```

```
datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                        query
-------+-------+----------+------+---------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 96374 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" LIMIT 1 OFFSET 1
 ```

 **break point 2.**

 ```
[2019-02-22 09:15:17.708 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 0.050 ms  statement: COMMIT
[2019-02-22 09:15:39.594 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 0.036 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 09:15:39.595 KST][96374][5c6f3ea2.17876][0]LOG:  duration: 0.171 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" LIMIT 1
```

```
 datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                   query
-------+-------+----------+------+---------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 96374 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" LIMIT 1
 ```

 **End Of Request**

특이한건 요청이 끝날때 커밋을 한번 더 침 ... (이건 확인 필요)

```
[2019-02-22 09:20:21.233 KST][97014][5c6f4029.17af6][0]LOG:  duration: 0.040 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 09:20:21.233 KST][97014][5c6f4029.17af6][0]LOG:  duration: 0.020 ms  statement: COMMIT
```

### How does transaction work when commit perform after select query and save query perform?

```python
@transaction.commit_manually
def tx_commit_manually(request):
    user = User.objects.all()[10]
    import ipdb; ipdb.set_trace() # break point 1.
    transaction.commit()
    user = User.objects.all()[11]
    user.username = 'tx-test-6'
    user.save()
    ipdb.set_trace()              # break point 2.
    transaction.commit()
```

**break point 1.**

```sql
[2019-03-15 23:40:59.087 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 0.140 ms  statement: SHOW default_transaction_isolation
[2019-03-15 23:40:59.088 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 0.437 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-03-15 23:40:59.088 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 0.030 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-03-15 23:40:59.089 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 1.437 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" LIMIT 1 OFFSET 10
```

**break point 2.**

```sql
[2019-03-15 23:41:03.824 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 0.045 ms  statement: COMMIT
[2019-03-15 23:41:07.047 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 0.043 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-03-15 23:41:07.048 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 0.193 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" LIMIT 1 OFFSET 11
[2019-03-15 23:41:17.245 KST][67646][5c8bb97b.1083e][0]LOG:  duration: 1.287 ms  statement: SELECT (1) AS "a" FROM "auth_user" WHERE "auth_user"."id" = 95378  LIMIT 1
[2019-03-15 23:41:17.251 KST][67646][5c8bb97b.1083e][456308]LOG:  duration: 2.375 ms  statement: UPDATE "auth_user" SET "username" = 'tx-test-6', "first_name" = '', "last_name" = '', "email" = 'haunter.poliwag@dev.null', "password" = 'sha1$zptElQq5jkPI$f2db6c66eaa0afaca1cf6f8f3ddc20e87675c172', "is_staff" = false, "is_active" = true, "is_superuser" = false, "last_login" = '2013-09-22 21:48:47.748010', "date_joined" = '2013-08-02 22:19:38.650860' WHERE "auth_user"."id" = 95378
[2019-03-15 23:41:17.273 KST][67646][5c8bb97b.1083e][456308]LOG:  duration: 2.313 ms  statement: SELECT "customer_userleavinginfo"."user_id", "customer_userleavinginfo"."is_deleted", "customer_userleavinginfo"."left_at", "customer_userleavinginfo"."reason", "customer_userleavinginfo"."is_dormant_user" FROM "customer_userleavinginfo" WHERE "customer_userleavinginfo"."user_id" = 95378
```

**break point 3.**

```sql
[2019-03-15 23:57:17.936 KST][68721][5c8bbc9a.10c71][0]LOG:  duration: 0.400 ms  statement: COMMIT
[2019-03-15 23:57:30.514 KST][68721][5c8bbc9a.10c71][0]LOG:  duration: 0.035 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-03-15 23:57:30.514 KST][68721][5c8bbc9a.10c71][0]LOG:  duration: 0.019 ms  statement: COMMIT
```

### How does transaction work transaction where query execute outside of commit_manually context manager?

```python
def tx_commit_manually(request):
    user = User.objects.latest('pk')
    import ipdb; ipdb.set_trace()

    with transaction.commit_manually():
        user = User.objects.get(username='tx_test_update')
        ipdb.set_trace()

        user.username = 'tx_test_save'
        user.save()
        ipdb.set_trace()

        transaction.commit()
        ipdb.set_trace() 
```

**break point 1.**

```
[2019-02-22 08:52:37.213 KST][93950][5c6f39c5.16efe][0]LOG:  duration: 0.206 ms  statement: SHOW default_transaction_isolation
[2019-02-22 08:52:37.214 KST][93950][5c6f39c5.16efe][0]LOG:  duration: 0.495 ms  statement: SET TIME ZONE 'Asia/Seoul'
[2019-02-22 08:52:37.214 KST][93950][5c6f39c5.16efe][0]LOG:  duration: 0.048 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:52:37.216 KST][93950][5c6f39c5.16efe][0]LOG:  duration: 2.145 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" ORDER BY "auth_user"."id" DESC LIMIT
```

```
datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                                   query
-------+-------+----------+------+---------+---------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 94191 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" ORDER BY "auth_user"."id" DESC LIMIT 1
 ```

 **break point 2.**

 ```
 [2019-02-22 08:54:17.416 KST][94191][5c6f3a22.16fef][305875]LOG:  duration: 0.922 ms  statement: INSERT INTO "auth_user" ("username", "first_name", "last_name", "email", "password", "is_staff", "is_active", "is_superuser", "last_login", "date_joined") VALUES ('tx_test_b', '', '', '', '', false, true, false, '2019-02-22 08:54:17.414420', '2019-02-22 08:54:17.414447') RETURNING "auth_user"."id"
[2019-02-22 08:54:17.418 KST][94191][5c6f3a22.16fef][0]LOG:  duration: 0.659 ms  statement: COMMIT
[2019-02-22 08:54:17.440 KST][94191][5c6f3a22.16fef][0]LOG:  duration: 0.035 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:54:17.441 KST][94191][5c6f3a22.16fef][0]LOG:  duration: 0.666 ms  statement: SELECT "customer_userleavinginfo"."user_id", "customer_userleavinginfo"."is_deleted", "customer_userleavinginfo"."left_at", "customer_userleavinginfo"."reason", "customer_userleavinginfo"."is_dormant_user" FROM "customer_userleavinginfo" WHERE "customer_userleavinginfo"."user_id" = 147994
[2019-02-22 08:54:17.442 KST][94191][5c6f3a22.16fef][0]LOG:  duration: 0.018 ms  statement: COMMIT
```

```
 datid |  pid  | usename  | app  | waiting | state  |                                               query
-------+-------+----------+------+---------+--------+----------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 94191 | postgres |      | f       | idle   | COMMIT
 ```

 **break point 3.**

```
 [2019-02-22 08:57:02.502 KST][94474][5c6f3ab9.1710a][0]LOG:  duration: 0.037 ms  statement: BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED
[2019-02-22 08:57:02.502 KST][94474][5c6f3ab9.1710a][0]LOG:  duration: 0.615 ms  statement: SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'tx_test_c'
```

``` 
datid |  pid  | usename  | app  | waiting |        state        |                                                                                                                                                                     query
-------+-------+----------+------+---------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active              | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 94474 | postgres |      | f       | idle in transaction | SELECT "auth_user"."id", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."password", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."is_superuser", "auth_user"."last_login", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = 'tx_test_c'
```

**break point 4.**

```
[2019-02-22 08:58:20.234 KST][94474][5c6f3ab9.1710a][0]LOG:  duration: 0.220 ms  statement: SELECT (1) AS "a" FROM "auth_user" WHERE "auth_user"."id" = 147996  LIMIT 1
[2019-02-22 08:58:20.238 KST][94474][5c6f3ab9.1710a][305878]ERROR:  duplicate key value violates unique constraint "auth_user_username_key"
[2019-02-22 08:58:20.238 KST][94474][5c6f3ab9.1710a][305878]DETAIL:  Key (username)=(tx_test_save) already exists.
[2019-02-22 08:58:20.238 KST][94474][5c6f3ab9.1710a][305878]STATEMENT:  UPDATE "auth_user" SET "username" = 'tx_test_save', "first_name" = '', "last_name" = '', "email" = '', "password" = '', "is_staff" = false, "is_active" = true, "is_superuser" = false, "last_login" = '2019-02-22 08:56:44.492716', "date_joined" = '2019-02-22 08:56:44.492749' WHERE "auth_user"."id" = 147996
```

```
 datid |  pid  | usename  | app  | waiting |             state             |                                                                                                                                                       query
-------+-------+----------+------+---------+-------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 16392 | 81912 | postgres | psql | f       | active                        | select datid, pid, usename, application_name as app, waiting, state, query  from pg_stat_activity;
 16392 | 94474 | postgres |      | f       | idle in transaction (aborted) | UPDATE "auth_user" SET "username" = 'tx_test_save', "first_name" = '', "last_name" = '', "email" = '', "password" = '', "is_staff" = false, "is_active" = true, "is_superuser" = false, "last_login" = '2019-02-22 08:56:44.492716', "date_joined" = '2019-02-22 08:56:44.492749' WHERE "auth_user"."id" = 147996
(3 rows)
```


## Performance 

### 트랜잭션을 지속적으로 열고 닫기 vs 한번 열고 닫기 

트랜잭션을 지속적으로 열고 닫는것과 한번 열고 모든 작업을 마친 후 닫는것의 성능차이는 얼마나 있을까?

#### 한번만 열고 닫기

```python
@transaction.commit_manually
def tx_commit_manually(request):
    begin = time.time()

    for i in range(1000):
        User.objects.create(username='tx_test_user_{}'.format(i))

    transaction.commit()

    print("--- %s seconds ---" % (time.time() - begin))
    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

위 결과는 다음과 같다.  

```
--- 7.35732483864 seconds ---
```

#### 지속적으로 열고 닫기 

```python
@transaction.commit_manually
def tx_commit_manually(request):
    begin = time.time()

    for i in range(1000):
        User.objects.create(username='tx_test_user_again{}'.format(i))
        transaction.commit()

    print("--- %s seconds ---" % (time.time() - begin))
    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

위 결과는 다음과 같다. 

```
--- 50.7602729797 seconds ---
```

### close_connection 사용 유무

#### 사용

```python
def tx_autocommit(request):
    begin = time.time()

    for i in range(1000):
        user = User.objects.all()[i]
        pk = user.pk

    print("--- %s seconds ---" % (time.time() - begin))
    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

```
--- 1.60926699638 seconds ---
```

```python
def tx_autocommit(request):
    begin = time.time()

    for i in range(1000):
        user = User.objects.all()[i]
        pk = user.pk
        close_connection()

    print("--- %s seconds ---" % (time.time() - begin))
    return JSONResponse({'result': 'ok'}, status=httplib.OK)
```

```
--- 11.8700170517 seconds ---
```
