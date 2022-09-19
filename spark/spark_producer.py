import requests
import os
import json
import numpy as np
import pandas as pd
import pyspark.pandas as ps
from unidecode import unidecode
import datetime
import time
from kafka import KafkaProducer

KAFKA_HOST='kafka:9092'

time.sleep(60)

class TwitterProducer:
    def __init__(self):
        self.token = 'AAAAAAAAAAAAAAAAAAAAADNVhAEAAAAAfgohmt4oXJK3eN5WFjzxMpDIUKY%3DGVdP4Fd6Zgvpxz5IvMmnjasTP7cSDz3VsswUBUTjXtUmZHwM3J'
        self.time()
        self.query_params = {'query': 'Lula OR Bolsonaro lang:pt ','max_results': '100','tweet.fields': 'created_at','start_time': self.start_time_str,'end_time': self.end_time_str}
        self.my_producer = KafkaProducer(bootstrap_servers = [KAFKA_HOST],value_serializer = lambda x:json.dumps(x).encode('utf-8'))
        self.search_url = "https://api.twitter.com/2/tweets/search/recent"
        
        self.main()
        
    def bearer_oauth(self,r):
        """
            Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.token}"
        r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        return r

    def connect_to_endpoint(self):
        response = requests.request("GET", self.search_url, auth=self.bearer_oauth, params=self.query_params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
    
    def time(self,booleana = True):
        if booleana:
            self.start_time = datetime.datetime.now() - datetime.timedelta(days = 6, hours = 20, minutes = 00)
        else:
            self.start_time = self.start_time + datetime.timedelta(days = 0, hours = 0, minutes = 4)
            
        self.end_time = self.start_time + datetime.timedelta(days = 0, hours = 0, minutes = 4)
        
        self.start_time_str = self.start_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z') + "Z"
        self.end_time_str = self.end_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z') + "Z"
        
    def get_data(self):
        self.json_response = self.connect_to_endpoint()
        
    def handle_data(self):
        self.spark_df = ps.DataFrame(self.json_response['data'])
        self.spark_df['text'] = self.spark_df['text'].apply(lambda x: x.lower())
        self.spark_df['text'] = self.spark_df['text'].apply(unidecode)
        self.spark_df['text'] = self.spark_df['text'].apply(lambda x: x.replace('\n',''))
        self.spark_df['text'] = self.spark_df['text'].apply(lambda x: x.replace('\t',''))
        self.spark_df['bolsonaro'] = self.spark_df['text'].apply(lambda x: x if x.find('bolsonaro') != -1 and x.find('lula') == -1 else '')
        self.spark_df['lula'] = self.spark_df['text'].apply(lambda x: x if x.find('lula') != -1 and x.find('bolsonaro') == -1 else '')    
        self.spark_df['lula_bolsonaro'] = self.spark_df['text'].apply(lambda x: x if x.find('lula') != -1 and x.find('bolsonaro') != -1 else '')
        self.spark_df = self.spark_df.drop(columns = ['id'])
        
        
    def main(self):
        
        while True:
            self.get_data()
            self.handle_data()

            for i in range(len(self.spark_df)):

                if self.spark_df['bolsonaro'][i] != '' and self.spark_df['lula_bolsonaro'][i] == '':
                    self.my_producer.send(value = self.spark_df['bolsonaro'][i],topic = 'bolsonaro')

                if self.spark_df['lula'][i] != '' and self.spark_df['lula_bolsonaro'][i] == '':
                    self.my_producer.send(value = self.spark_df['lula'][i],topic = 'lula')
                
                if self.spark_df['lula_bolsonaro'][i] != '':
                    self.my_producer.send(value = self.spark_df['lula_bolsonaro'][i],topic = 'lula_bolsonaro')
            
            
            self.time(booleana = False)
            self.query_params['start_time'] = self.start_time_str
            self.query_params['end_time'] = self.end_time_str

TwitterProducer()       
        
