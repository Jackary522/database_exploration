# Log into Postgres Metastore container
docker exec -it hive-metastore-postgresql /bin/bash

# Become the user postgres
su - postgres

# Connect to Postgres database instance
psql

# Verify the user hive exists by executing the following from the psql prompt
\du

# Create the metastore database 
create database metastore;

# Change ownership of the database to user hive
alter database metastore owner to hive;

# alter user to grant full permissions
alter user hive with superuser createdb createrole login;

# Logout of psql
\q

# Create database objects for metastore database
psql -d metastore -f /hive/hive-schema-2.3.0.postgres.sql
psql -d metastore -f /hive/hive-txn-schema-2.3.0.postgres.sql
psql -d metastore -f /hive/upgrade-2.3.0-to-3.0.0.postgres.sql
psql -d metastore -f /hive/upgrade-3.0.0-to-3.1.0.postgres.sql
