# FM Database 

## Commands

To see all available commands type: `fm_database`

### Working with Alembic
This package uses alembic to help with database creations and migrations.
Some commands are encorporated into the cli (eg. the subcommands found in `fm_database update`).

To fall back to the alembic program you need to pass the configuration file.

```console
(database) fm@52b5684f4ca7:/workspaces/database$ alembic -c migrations/alembic.ini current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
d09ea0b9c0c0 (head)
````