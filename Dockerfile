FROM python:3.10

WORKDIR /tempLogger

COPY ./src ./src
COPY ./secrets ./secrets
COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR ./src

ENTRYPOINT ["python", "templogger.py"]
