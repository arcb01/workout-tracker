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

    # FIXME: Update with the new pipeline
    # TODO: Updation phase: checking for duplicates
    # FIXME: Validation schema not working

    w_data = generate_workouts_data()

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

    # ------ Load environment variables ------
    load_dotenv()
    config = dotenv_values("./.env/.env")

    NOTION_TOKEN = config["NOTION_TOKEN"]
    DATABASE_ID = "3badcbc40d434e00835bd09930f4a801"

    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # Database connection
    client = MongoClient("mongodb://192.168.0.32:2717/")
    db = client["gym"]
    exs_collection = db["exs"]
    wsns_collection = db["wsns"]

    print(exs_collection.count_documents({}))
    print(wsns_collection.count_documents({}))

    # 1. Create collection + validation schema
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
