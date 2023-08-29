from modules.notion_api import *
import pprint
import os 
import random
import string
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from mongo_utils import *


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

# ------------------ Data preprocessing ------------------

def workout_formatter(workout : dict):
    """
    Formats the workout data to a more legible structure.
    """

    workout_date = workout["properties"]["Date"]["date"]["start"]
    workout_intensity = workout["properties"]["Intensity"]["select"]["name"]
    workout_location = workout["properties"]["Location"]["select"]["name"]
    workout_duration = workout["properties"]["Duration"]["number"]

    return { 
            "date" : datetime.strptime(workout_date, '%Y-%m-%d'),
            "intensity" : workout_intensity,
            "location" : workout_location,
            "duration" : workout_duration,
            "exercises" : exercise_formatter(workout)
            }


def exercise_formatter(workout : dict):
    """
    Formats the exercises data to a more legible structure.
    """

    workout_exercises = []
    # Get the id of the database that contains the exercises
    ex_db_id = read_page(workout["id"], headers)["results"][0]["id"]
    # Database containing all the exercises
    workout_ex_db = read_database(ex_db_id, headers)["results"]
    num_exercises = len(workout_ex_db)

    # Loop through all the exercises in the workout and format them
    for n in range(num_exercises):
        workout_ex_name = workout_ex_db[n]["properties"]["Name"]["title"][0]["plain_text"]
        workout_ex_sets = workout_ex_db[n]["properties"]["Sets"]["number"]
        workout_ex_reps = workout_ex_db[n]["properties"]["Reps"]["number"]
        workout_ex_weight = workout_ex_db[n]["properties"]["Weight"]["number"]
        workout_ex_data = { 
                            "w_id" : "", # TBA
                            "name" : workout_ex_name,
                            "sets" : workout_ex_sets,
                            "reps" : workout_ex_reps,
                            "weight" : workout_ex_weight,
                        }

        workout_exercises.append(workout_ex_data)

    return workout_exercises

def generate_workouts_data():
    """
    Generates all the workouts data.
    """
    
    data = []

    wts_db_data = read_database(DATABASE_ID, headers)["results"]
    
    # Format each workout as well as its exercises
    for workout in wts_db_data:
        data.append(workout_formatter(workout))

    print("Succesfully workouts data generated.")

    return data


def insert_data_db(db):

    # FIXME: Not sure

    w_data = generate_workouts_data()

    wsns_collection = db["wsns"]
    exs_collection = db["exs"]

    for wokrout in w_data:
        workout_exercises = wokrout["exercises"]
        for exercise in workout_exercises:
            # Empty the workout exercises list
            wokrout["exercises"] = []
            # Add the workout id to the exercise
            workout_id = wsns_collection.insert_one(wokrout).inserted_id
            exercise["w_id"] = workout_id

            # Check if exercise already exists
            existing_exercise = exs_collection.find_one(exercise)
            if not existing_exercise:
                # Insert the exercise
                exs_collection.insert_one(exercise)
                # update the workout document apending the exercise id to the exercises list
                wsns_collection.update_one({"_id": workout_id}, {"$push": {"exercises": exercise["_id"]}})


        


if __name__ == "__main__":

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
    show_collection(exs_collection)

    client.close()
