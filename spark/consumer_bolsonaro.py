import json 
from kafka import KafkaConsumer
import random
from datetime import datetime
import time 
import os
import sys

from elasticsearch import Elasticsearch

ELASTIC_SEARCH_HOST='http://es01:9200'
KAFKA_HOST='kafka:9092'

time.sleep(60)


es = Elasticsearch(ELASTIC_SEARCH_HOST)
if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'bolsonaro',
        bootstrap_servers=KAFKA_HOST,
        #auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )



    
    for message in consumer:
    #    print(json.loads(message.value))

       doc = {
             "text": f"{message.value}",
             "timestamp": datetime.now()}
       
       res = es.index(index="bolsonaro", body=doc)
       print(res['result'])