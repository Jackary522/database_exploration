
# PostrgreSQL Statistics Tables

For an example, we will see the row count of the contacts table.

```
contacts=# select count(*) from contacts;

8322476
```

By default, the statistics table zeroes out on restore. Therefire w must update the stats tables. Otherwise, it will be as shown below.

```
contacts=# select relname, n_live_tup, n_dead_tup from pg_stat_user_tables;

    relname | n_live_tup | n_dead_tup
------------+------------+-------------
contacts    |          0 |          0
contacts_sm |          0 |          0
contacts_ts |          0 |          0
(3 rows)
```

To fix this issue, and therefore increase query speeds, run `analyze table` so that the statistics can be up to date.


```
contacts=# analyze contacts;

contacts=# select relname, n_live_tup, n_dead_tup from pg_stat_user_tables;

    relname | n_live_tup | n_dead_tup
------------+------------+------------|
contacts    |    8321800 |          0
contacts_sm |          0 |          0
contacts_ts |          0 |          0
(3 rows)
```

Analyze updates the statistics table so that query plans can be accurate.

```
contacts=# \x
contacts=# select * from pg_stat_user_tables where relname like 'contacts%';
```

`\x` opens in expanded mode


```
contacts=# select relname, reloptions from contacts.pg_catalog.pg_class where relname = 'contacts';
```




