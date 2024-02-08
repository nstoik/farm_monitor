# FM SERVER 

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