FROM python:3.8


WORKDIR /app/
RUN pip3 install kafka-python requests python-dateutil unidecode pyspark pandas numpy
RUN pip3 install pyarrow
RUN apt update
RUN apt install -y default-jre default-jdk
COPY spark_producer.py main.py

CMD ["python3", "main.py"]