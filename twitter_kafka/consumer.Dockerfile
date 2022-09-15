FROM python:3.8


WORKDIR /app/
COPY consumer.py main.py
RUN pip3 install kafka-python

CMD ["python3", "main.py"]