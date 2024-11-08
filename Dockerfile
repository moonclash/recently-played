FROM python:3.9.18-slim

WORKDIR /recently-played

COPY ./src/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src/ .

RUN touch db.json

CMD uvicorn main:app --host 0.0.0.0 --port $PORT