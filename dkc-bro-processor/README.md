# DKC-BRO Processor
## Setup local development environment
Dependencies:
1. [Python](https://www.python.org/) - Python 3.12 is recommended.
2. [Docker](https://www.docker.com/) - Docker for a seamless development experience. Alternatively, you can just use PDM package manager or any local venv.
3. [PDM](https://pdm-project.org/) PDM is a package manager, for adding new packages to the project. Install with `pip install --user pdm`. If you're not planning to add new dependencies, you can also just use pip with the generated `requirements.txt` file.
4. [Make](https://www.gnu.org/software/make/) - Make is used to simplify the development process. If you don't have make installed, you can run the commands manually.

## Debugging on VS Code
Debugging FastAPI applications is possible without extra configuration. See https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger.

## Start development environment (using Docker)
0. Make sure you are in the backend folder. `cd backend`
1. Configure environment configuration: `cp .env.example .env`. A `.env` file is created.
2. Start the db: `docker compose up -d db dbgate`. Wait for the database to fully start.
3. Update the db: `pdm run alemibc upgrade head`

## Create new revision based on models
1. `alembic revision --autogenerate -m "{revision_message}"`

## Pre-commit
To enable pre-commit use `pdm pre-commit install`
For autoupdate use `pdm run pre-commit autoupdate`
For using on all files `pdm run pre-commit run --all-files -v` 

## Typecheck, format and lint
We use pyright and ruff for typechecking, formatting and linting. See the Makefile for the commands in the backend folder. 

