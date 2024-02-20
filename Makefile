lint: 
	black .
	ruff check . --fix
	isort .
