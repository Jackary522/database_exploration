create database if not exists contacts;
use contacts;
CREATE TABLE contacts
(
    contactID int,
    firstName string,
    lastName string,
    areacode string,
    phone string,
    email string
)
row format delimited
fields terminated by '~'
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/contacts.db/contacts';

