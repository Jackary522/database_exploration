
-- Question 1: Create a new table named chicago_contacts (areacode = 312)

create table chicago_contacts
(
    serial_id  serial primary key,
    contact_id int references contacts(contact_id)
);

insert into chicago_contacts
    select contact_id
    from contacts
    where areacode = '312';

------------------------------------------------------------------------------------------------------------------------

-- Question 2: Create a temporary table named contacts_temp

-- Load the first 1000 rows from the contact table into the temporary table
create temp table contacts_temp as
    select *
    from contacts
    limit 1000;

-- Query the count for the table
select count(*)
from contacts_temp;
-- count = 1000

-- Search for the temp table in the statistics table
select relid, relname, n_live_tup
from contacts.pg_catalog.pg_stat_user_tables
where relname = 'contacts_temp';

-- Shutdown Postgres

-- Query the count for the table
select count(*)
from contacts_temp;
-- no contacts_temp table

-- Search for the temp table in the statistics table
select relid, relname, n_live_tup
from contacts.pg_catalog.pg_stat_user_tables
where relname = 'contacts_temp';
-- no contacts_temp table

------------------------------------------------------------------------------------------------------------------------

-- Question 3: Create an index on the column lastname.
-- Determine how often the index was used.
-- Run the query below.

create index idx_lastname on contacts (lastname);

select *
from contacts
where lastname = 'Bryson';

select idx_scan
from contacts.pg_catalog.pg_stat_user_indexes
where indexrelname = 'idx_lastname';

------------------------------------------------------------------------------------------------------------------------

-- Question 4: Write a query to get the size of the database and the size of the contacts table

select pg_size_pretty(pg_database_size('contacts')) as database_size;

select pg_size_pretty(pg_total_relation_size('contacts')) as table_size;

------------------------------------------------------------------------------------------------------------------------

-- Question 5: Get the size of the column areacode.
-- Convert the column to "int" and get the size of the column again.

select sum(pg_column_size(areacode)) as column_size
from contacts;

alter table contacts
alter column areacode type int using areacode::int;

select sum(pg_column_size(areacode)) as coloumn_size
from contacts;

------------------------------------------------------------------------------------------------------------------------

-- Question 6: Run explain analyze for the following query:
--     select * from contacts where contact_id = 10081;
-- Create an index on contact_id and run explain again.

explain analyze select * from contacts where contact_id = 10081;

-- Gather  (cost=1000.00..143319.58 rows=1 width=64) (actual time=0.900..868.412 rows=1 loops=1)
--   Workers Planned: 2
--   Workers Launched: 2
--   ->  Parallel Seq Scan on contacts  (cost=0.00..142319.48 rows=1 width=64) (actual time=570.372..859.332 rows=0 loops=3)
--         Filter: (contact_id = 10081)
--         Rows Removed by Filter: 2774158
-- Planning Time: 3.652 ms
-- Execution Time: 868.748 ms

create index on contacts(contact_id);

explain analyze select * from contacts where contact_id = 10081;

-- Index Scan using contacts_contact_id_idx on contacts  (cost=0.43..8.45 rows=1 width=64) (actual time=0.035..0.036 rows=1 loops=1)
--   Index Cond: (contact_id = 10081)
-- Planning Time: 0.313 ms
-- Execution Time: 0.055 ms

------------------------------------------------------------------------------------------------------------------------

-- Question 7: Select the estimated row count for the table Contacts
-- not using "select count(*) from contacts"

select n_live_tup
from contacts.pg_catalog.pg_stat_user_tables
where relname = 'contacts';

-- 8315967

------------------------------------------------------------------------------------------------------------------------

-- Question 8: Delete 30,000 rows from the contacts table and list
--     the number of dead tuples and the size of the table (analyze must be executed)

delete from contacts where contact_id in (select contact_id from contacts limit 30000);
analyze contacts;

-- Run pgstattuple on the table

select * from pgstattuple('contacts');

-- Run vacuum on the table and list the number of dead tuples and the size
--     of the table (analyze must be executed)

vacuum analyze contacts;

-- Run pgstattuple on the table

select * from pgstattuple('contacts');

-- Run vacuum full on the table and list teh number of live and dead tuples
--     and the size of the table (analyze must be executed)

vacuum full analyze contacts;

-- Get the size for the table

select pg_size_pretty(pg_total_relation_size('contacts')) as table_size;

-- Run pgstattuple on the table

select * from pgstattuple('contacts');

------------------------------------------------------------------------------------------------------------------------

-- Question 9: Create an index on the column areacode

create index areacode_index on contacts (areacode);
analyze contacts;

-- Get the size of the index

select pg_size_pretty(pg_total_relation_size('areacode_index'));

-- Run explain on the query: select * from contacts where areacode = '801';

explain select * from contacts where areacode = '801';

-- Bitmap Heap Scan on contacts  (cost=222.46..49568.90 rows=19874 width=64)
--   Recheck Cond: ((areacode)::text = '801'::text)
--   ->  Bitmap Index Scan on areacode_index  (cost=0.00..217.49 rows=19874 width=0)
--         Index Cond: ((areacode)::text = '801'::text)

-- Create an index for UT area codes

create index ut_areacodes on contacts (areacode) where areacode = '801';

-- Get the size of the index

select pg_size_pretty(pg_total_relation_size('ut_areacodes'));

-- Run explain on the query: select * from contacts where areacode = '801';

explain select * from contacts where areacode = '801';

-- Bitmap Heap Scan on contacts  (cost=180.63..49527.07 rows=19874 width=64)
--   Recheck Cond: ((areacode)::text = '801'::text)
--   ->  Bitmap Index Scan on ut_areacodes  (cost=0.00..175.66 rows=19874 width=0)

------------------------------------------------------------------------------------------------------------------------

-- Question 10: Alter the table contacts by adding a text column named mydata
-- Get the size of the table before and after the alter

select pg_size_pretty(pg_total_relation_size('contacts'));

alter table contacts
add column mydata text;

-- 1105 MB

-- Update the table by adding the sentence: "Fear is the mind killer."

update contacts
set mydata = 'Fear is the mind killer';

-- Get the size of the table

select pg_size_pretty(pg_total_relation_size('contacts'));

-- 2205 MB