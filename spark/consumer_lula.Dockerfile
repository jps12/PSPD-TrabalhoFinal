FROM python:3.8


WORKDIR /app/
RUN pip3 install kafka-python elasticsearch==7.14.0

COPY consumer_lula.py main.py

CMD ["python3", "main.py"]