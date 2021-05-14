poetry new myfastapi
poetry add uvicorn
poetry add fastapi
poetry add pydantic[email]

poetry run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

poetry env
poetry env info --path
tą ścieżkę kopiujemy do vscode: > select interpreter python
> select linter > flake8
> 
