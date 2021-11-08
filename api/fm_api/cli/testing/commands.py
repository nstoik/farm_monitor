"""Command line interface for testing and linting."""
import os
import sys
from glob import glob
from subprocess import PIPE, call, run

import click

from fm_api.settings import get_config

config = get_config()  # pylint: disable=invalid-name
APP_DIR = config.APP_DIR
PROJECT_ROOT = config.PROJECT_ROOT
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
@click.option(
    "-c",
    "--coverage",
    default=False,
    is_flag=True,
    help="Run tests with coverage",
)
@click.option(
    "-f",
    "--filename",
    default=None,
    help="Run a specific test file. eg. 'tests/test_forms.py'",
)
@click.option(
    "-k",
    "--function",
    default=None,
    help="Run tests by name eg. 'test_get_by_id' or 'test_get_by_id or test_validate_success'",
)
def test(coverage, filename, function):
    """Run the tests."""

    pytest_args = []

    if filename:
        pytest_args.extend([filename, "--verbose"])
    else:
        pytest_args.extend([TEST_PATH, "--verbose"])
    if function:
        pytest_args.extend(["-k", function])
    if coverage:
        pytest_args.extend(["--cov", PROJECT_ROOT])
        pytest_args.extend(["--cov-report", "term-missing:skip-covered"])

    # Get the virtual environment to the path for subprocess calls
    pipenv_path = run(["pipenv", "--venv"], check=True, stdout=PIPE)
    pipenv_path = pipenv_path.stdout.decode().replace("\n", "")
    pipenv_path = os.path.join(pipenv_path, "bin")

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""

        # Add the virtual environment to the path for subprocess calls
        my_env = os.environ.copy()
        my_env["PATH"] = os.pathsep.join([pipenv_path, my_env["PATH"]])

        command_line = list(args)
        click.echo(f"{description}: {' '.join(command_line)}")
        rv = call(command_line, env=my_env)
        return rv

    previous_env_database = os.getenv("FM_DATABASE_CONFIG", default="dev")
    previous_env_frontend = os.getenv("FM_API_CONFIG", default="dev")
    os.environ["FM_DATABASE_CONFIG"] = "test"
    os.environ["FM_API_CONFIG"] = "test"

    rv = execute_tool("Run pytest", "pytest", *pytest_args)

    os.environ["FM_DATABASE_CONFIG"] = previous_env_database
    os.environ["FM_API_CONFIG"] = previous_env_frontend

    sys.exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8 and isort."""
    skip = [
        "requirements",
        "migrations",
        "__pycache__",
        "node_modules",
        "build",
        "fm_api.egg-info",
        "assets",
    ]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    # Get the virtual environment to the path for subprocess calls
    pipenv_path = run(["pipenv", "--venv"], check=True, stdout=PIPE)
    pipenv_path = pipenv_path.stdout.decode().replace("\n", "")
    pipenv_path = os.path.join(pipenv_path, "bin")
    my_env = os.environ.copy()
    my_env["PATH"] = os.pathsep.join([pipenv_path, my_env["PATH"]])

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo(f"{description}: {' '.join(command_line)}")
        rv = call(command_line, env=my_env)
        if rv != 0:
            sys.exit(rv)

    isort_args = ["--profile", "black"]
    black_args = ["--diff"]
    mypy_args = ["--warn-unused-ignores", "--show-error-codes"]
    pylint_args = ["--load-plugins", ""]
    if check:
        isort_args.append("--check")
        black_args.append("--check")
        # mypy_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")
    execute_tool("Checking for code errors", "pylint", *pylint_args)
    execute_tool("Checking static types", "mypy", *mypy_args)
