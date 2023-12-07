# Log into Hive server container
docker exec -it hive-server /bin/bash

# cd to /contacts directory 
# (It is directly mapped and shared to contacts on your laptop)
cd /contacts

# Execute the contacts_table.hql to create a new external hive table contacts 
# ins the new database contacts.
hive -f contacts.hql

# Now, let’s add some data to this hive table. For that, simply push the contacts.csv present in the contacts directory on the hive-server into HDFS.
hadoop fs -put contacts.csv hdfs://namenode:8020/user/hive/warehouse/contacts.db/contacts

# Connect to beeline (login is hive and password is hive)
beeline
!connect jdbc:hive2://

# Verify the contacts database exists while logged into beeline
show databases

# Connect to the contacts database
use contacts;

# Verify the contact table exists
show tables;

# Verify the data is on the tables
select * from contacts;