# FM Database 

## Commands

To see all available commands type: `fm_database`

```bash
> cd database
> pipenv shell
> pipenv install --dev
> fm_database
Usage: fm_database [OPTIONS] COMMAND [ARGS]...

  Entry point for CLI.

Options:
  --help  Show this message and exit.

Commands:
  create  Command group for database create commands.
  lint    Lint and check code style with black, flake8 and isort.
  test    Run the tests.
  update  Command group for database update commands.
```

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