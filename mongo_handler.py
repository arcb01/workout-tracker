from notion_utils import *
import pprint
import os 
import random
import string
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from mongo_utils import *
from preprocess import preprocess


def update_db(db : object):
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
          
if __name__ == "__main__":

    # Database connection
    client = MongoClient("mongodb://192.168.0.32:2717/")
    db = client["gym"]

    # Insert data
    update_db(db)

    client.close()
