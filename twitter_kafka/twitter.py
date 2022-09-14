from cgitb import text
import requests
import os
import sys
import json
import datetime
import dateutil.parser as parser
# from dotenv import load_dotenv
# load_dotenv()
from kafka import KafkaProducer

bearer_token = 'AAAAAAAAAAAAAAAAAAAAADNVhAEAAAAAfgohmt4oXJK3eN5WFjzxMpDIUKY%3DGVdP4Fd6Zgvpxz5IvMmnjasTP7cSDz3VsswUBUTjXtUmZHwM3J'

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields




def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def parser_time(time):
    return  parser.parse(str(time)).isoformat() + "Z"

def get_tweets(number=1000):
    my_producer = KafkaProducer(  
    bootstrap_servers = ['localhost:9092'],  
    value_serializer = lambda x:json.dumps(x).encode('utf-8')  
    )  
    tod = datetime.datetime.now()
    d = datetime.timedelta(days = 6, hours = 20, minutes = 00)
    d_min = datetime.timedelta(days = 0, hours = 0, minutes = 2)
    start = tod - d
    while(number > 0):
        print("Number of tweets left: " + str(number))
        print("Start time: " + str(start))
        print("are missing: " + str(number))
        print("processing...") #+ str(100-((number/int(sys.argv[1]))*100)) + "%")
        if(number <= 100):
            query_params = {'query': 'Lula OR Bolsonaro lang:pt ','max_results': number,'tweet.fields': 'created_at','start_time': parser_time(start),'end_time': parser_time(start + d_min)}
        else:
            query_params = {'query': 'Lula OR Bolsonaro lang:pt ','max_results': '100','tweet.fields': 'created_at','start_time': parser_time(start),'end_time': parser_time(start + d_min)}
        number -= 100
        json_response = connect_to_endpoint(search_url, query_params)
        for i in json_response['data']:
            if(i['text'].find('Lula') != -1 or i['text'].find('lula') != -1 and i['text'].find('Bolsonaro') != -1 or i['text'].find('bolsonaro') != -1):
                my_producer.send(topic='test', value=i['text'])
            elif(i['text'].find('test') != -1 or i['text'].find('Lula') != -1):
                my_producer.send(value=i['text'], topic='lula')
            elif(i['text'].find('test') != -1 or i['text'].find('Bolsonaro') != -1):
                my_producer.send(value=i['text'], topic='test')
        start  += d_min
        print(("_____________________"))
    print("Done!")
    return True


if __name__ == "__main__":
    get_tweets()