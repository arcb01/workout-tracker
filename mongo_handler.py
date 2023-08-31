from notion_utils import *
import pprint
import os 
import random
import pandas as pd
import string
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from mongo_utils import *
from preprocess import preprocess


client = MongoClient("mongodb://192.168.0.32:2717/")
db = client["gym"]


def update_db():
    """
    Inserts data into the database.
    """

    # 1. Get preprocessed data from notion
    preprocess()

    # 2. Read clean data
    with open("./data/workouts_data.json", "r") as f:
        w_data = json.load(f)

    # Prepare database collections
    wsns_collection = db["wsns"]
    exs_collection = db["exs"]

    # 2. Insert data
    # FIXME: (Maybe this part could be done in a better way)
    # 2.1 Remove old data
    wsns_collection.delete_many({})
    exs_collection.delete_many({})
    # 2.2 Insert new data
    for wokrout in w_data:
        workout_exercises = wokrout["exercises"]
        # Insert exercises into exs collection
        exs_ids = exs_collection.insert_many(workout_exercises)
        wokrout["exercises"].clear()
        # Insert exs ids into workout exercises
        wokrout["exercises"] = exs_ids.inserted_ids
        wsns_collection.insert_one(wokrout)

    print("Data inserted successfully")
          

def get_plot_data():
    """
    Returns the data to be plotted.
    """

    # Number of workouts per month
    query = [
    {
        '$project': {
            'month': {'$month': {'date': {'$dateFromString': {'dateString': '$' + "date"}}}},
        }
    },
    {
        '$group': {
            '_id': '$month',
            'n_workouts': {'$sum': 1}
        }
    },
    {
        '$project': {
            '_id': 0,  
            'month': '$_id',  
            'n_workouts': '$n_workouts' 
        }
    },
    {
        '$sort': {'month': 1}
    }
]

    results = list(db["wsns"].aggregate(query))

    return results