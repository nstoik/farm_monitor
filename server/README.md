# FM SERVER 

This is the server component of the FM project. It has two main components: the server and the worker.

To run the server set the `FM_SERVER_RUN=true` environment variable that is checked in the [`start.sh`](start.sh) script.

To run the worker set the `FM_SERVER_RUN_WORKER=true` environment variable that is checked in the [`start.sh`](start.sh) script.


## Commands

To see all available commands type: `fm_server`

```bash
> cd server
> pipenv shell
> pipenv install --dev
> fm_api
Usage: fm_server [OPTIONS] COMMAND [ARGS]...

  Entry point for CLI.

Options:
  --help  Show this message and exit.

Commands:
  device       Command group for device commands.
  first-setup  First time setup.
  lint         Lint and check code style with black, flake8 and isort.
  run          Run the server.
  run-worker   Run the Celery worker.
  test         Run the tests.
```