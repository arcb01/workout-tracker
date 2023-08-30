from modules.notion_utils import *
import pprint
import os 
import random
import string
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from mongo_utils import *


def insert_data_db(db):

    # TODO: Updation phase: checking for duplicates
    # FIXME: Validation schema not working

    # Read clean data
    with open("./data/workouts_data.json", "r") as f:
        w_data = json.load(f)

    wsns_collection = db["wsns"]
    exs_collection = db["exs"]

    for wokrout in w_data:
        workout_exercises = wokrout["exercises"]
        # Insert exercises into exs collection
        exs_ids = exs_collection.insert_many(workout_exercises)
        wokrout["exercises"].clear()
        # Insert exs ids into workout exercises
        wokrout["exercises"] = exs_ids.inserted_ids
        wsns_collection.insert_one(wokrout)

if __name__ == "__main__":

    # Database connection
    client = MongoClient("mongodb://192.168.0.32:2717/")
    db = client["gym"]
    exs_collection = db["exs"]
    wsns_collection = db["wsns"]

    print(exs_collection.count_documents({}))
    print(wsns_collection.count_documents({}))

    # 1. Create collection + FIXME validation schema
    create_collection(db, "exs")
    create_collection(db, "wsns")

    # 2. Insert data
    insert_data_db(db)

    print(exs_collection.count_documents({}))
    print(wsns_collection.count_documents({}))

    # 3. Show data
    show_collection(wsns_collection)
    #show_collection(exs_collection)

    client.close()
