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
TOPIC='bolsonaro'

time.sleep(60)
words_black_list = {
    "em",
    "rt",
    "do",
    "da",
    "de",
    "e",
    "o",
    "a",
    "que",
    "com",
    "no",
    "na",
    "para",
    "um",
    "tem",
    "se",
}

es = Elasticsearch(ELASTIC_SEARCH_HOST)
if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_HOST,
        #auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    for message in consumer:
    #    print(json.loads(message.value))

        for word in message.value.split(' '):
            if word in words_black_list:
                continue
            doc = {
                    "text": f"{word}",
                    "timestamp": datetime.now()
            }
            
            res = es.index(index=TOPIC, body=doc)
            print(res['result'])