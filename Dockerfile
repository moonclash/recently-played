FROM python:3.9.18-slim

WORKDIR /recently-played

COPY ./src/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]