import json 
from kafka import KafkaConsumer
import random
from datetime import datetime
import time 
import os
import sys

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'test',
        bootstrap_servers='localhost:9092',
        #auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    
    for message in consumer:
       print(json.loads(message.value))
