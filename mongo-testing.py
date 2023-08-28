import json
from pymongo import MongoClient


with open('./data/a.json', 'r') as f:
    data = json.load(f)
    w_ssn_data = data['WRKT_SSNS']
    ex_data = data['EXERCISES']


# Connect to MongoDB
client = MongoClient('mongodb://192.168.0.32:2717/')
db = client['gym']


client.close()
