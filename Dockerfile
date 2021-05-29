FROM python:3.9-slim

RUN mkdir /app 
COPY poetry.lock pyproject.toml /app/
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

EXPOSE 5000

CMD poetry run uvicorn src.main.app:app --reload --host 0.0.0.0 --port 5000