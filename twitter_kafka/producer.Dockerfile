FROM python:3.8


WORKDIR /app/
COPY twitter.py main.py
RUN pip3 install kafka-python requests python-dateutil

CMD ["python3", "main.py"]