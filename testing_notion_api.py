from modules.notion_api import *
import pprint
import os 
import random
import string
from dotenv import load_dotenv, dotenv_values


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

    workout_id = workout["id"]
    workout_date = workout["properties"]["Date"]["date"]["start"]
    workout_intensity = workout["properties"]["Intensity"]["select"]["name"]
    workout_location = workout["properties"]["Location"]["select"]["name"]
    workout_duration = workout["properties"]["Duration"]["number"]

    return {"w_id" : workout_id,
            "date" : workout_date,
            "intensity" : workout_intensity,
            "location" : workout_location,
            "duration" : workout_duration,
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
        workout_ex_id = workout_ex_db[n]["id"]
        workout_ex_name = workout_ex_db[n]["properties"]["Name"]["title"][0]["plain_text"]
        workout_ex_sets = workout_ex_db[n]["properties"]["Sets"]["number"]
        workout_ex_reps = workout_ex_db[n]["properties"]["Reps"]["number"]
        workout_ex_weight = workout_ex_db[n]["properties"]["Weight"]["number"]
        workout_ex_data = { "w_id" : workout["id"],
                            "ex_id" : workout_ex_id,
                            "ex_name" : workout_ex_name,
                            "sets" : workout_ex_sets,
                            "reps" : workout_ex_reps,
                            "weight" : workout_ex_weight,
                        }

        workout_exercises.append(workout_ex_data)

    return workout_exercises


def generate_workouts_data():
    """
    Generates a json file containing all the workouts data.
    The JSON file has 2 collections: Workout Sessions and Exercises.
    """

    all_workouts = { "WRKT_SSNS" : [],
                    "EXERCISES" : []}
    
    wts_db_data = read_database(DATABASE_ID, headers)["results"]
    
    for workout in wts_db_data:
        all_workouts["WRKT_SSNS"].append(workout_formatter(workout))
        all_workouts["EXERCISES"].append(exercise_formatter(workout))

    # Save the data to a json file
    with open("./data/workouts_data.json", "w", encoding="utf8") as f:
        json.dump(all_workouts, f, ensure_ascii=False)

    print("Succesfully workouts data generated.")

generate_workouts_data()