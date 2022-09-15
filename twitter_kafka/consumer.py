import json 
from kafka import KafkaConsumer
import random
from datetime import datetime
import time 
import os
import sys
from time import sleep

sleep(30)

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'test',
        bootstrap_servers='kafka:9092'
        # auto_offset_reset='earliest'
    )

    list_message = []
    count = 0

    
    for message in consumer:
       time_to_sleep = random.randint(1, 20)
       time.sleep(time_to_sleep)
    
       print('recebi')
       print(message)
    #    list_message.append(json.loads(message.value))

    #    print('------------------------------------------------------------------------------------------')
    #    print(list_message)

    
        
        

    