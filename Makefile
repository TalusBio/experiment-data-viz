.venv:
	poetry install

format: .venv
	poetry run isort .
	poetry run black .
	poetry run flake8 .