## poetry commands
```ps
poetry new myfastapi
# ex:
poetry add uvicorn
poetry add fastapi
poetry add pydantic[email]

# run
poetry run uvicorn src.main.app:app --reload --host 0.0.0.0 --port 5000

# konf VS Code
poetry env
poetry env info --path
# tą ścieżkę kopiujemy i wklejamy jako interpreter 
# > select interpreter python
# > select linter > flake8

# Installing dependencies:
poetry install

poetry shell
```

## formatowanie / sortowanie importów
```sh
poetry shell 
isort .
black .
```


# docker 
```ps
docker build --tag marekprezes/moviedb .
docker run --rm marekprezes/moviedb sleep 10000 # for debug
docker run --rm --publish 5000:5000 marekprezes/moviedb
```

