format:
	pdm run ruff check --select I --fix
	pdm run black .
check: 
	pdm run pyright	
	pdm run black --check .
	pdm run ruff check
	pdm run ruff check --select I
pytest:
	pdm run pytest tests
api:
	uvicorn app.main:app --reload --port 8006