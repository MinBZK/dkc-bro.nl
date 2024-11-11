dev_poller:
	uvicorn app.main_poller:app --reload --port 8001
dev_dkc:
	uvicorn app.main:app --reload --port 8000
dev_db:
	docker compose up -d dbgate && docker compose up -d db-dkcbro
dev_db_reset:
	docker compose down && docker volume rm expert_service_database && docker compose up -d dbgate
dev_migration:
	alembic -c alembic/alembic.ini upgrade head
app_dkc_bro:
	docker compose up -d
test:
	python3 -m pytest tests
type_fix:
	python3 -m isort app
	python3 -m black app
	python3 -m ruff app
	python3 -m isort tests
	python3 -m black tests
	python3 -m ruff tests