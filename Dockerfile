FROM python:3.10

WORKDIR /tempLogger

COPY * .

RUN pip install < /requirements.txt

CMD ["python", "./tempLogger.py"]
