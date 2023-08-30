from dotenv import load_dotenv, dotenv_values
from modules.notion_utils import *
import json


def get_notion_data():
    """
    Get the data from Notion database.
    """

    wts_db_data = read_database(DATABASE_ID, HEADERS)["results"]

    return wts_db_data
    

def exercise_formatter(workout : dict):
    """
    For a given workout, formats the exercises data to a more legible structure.
    """

    workout_exercises = []
    # Get the id of the database that contains the exercises
    ex_db_id = read_page(workout["id"], HEADERS)["results"][0]["id"]
    # Database containing all the exercises
    workout_ex_db = read_database(ex_db_id, HEADERS)["results"]
    num_exercises = len(workout_ex_db)

    # Loop through all the exercises in the workout and format them
    for n in range(num_exercises):
        workout_ex_name = workout_ex_db[n]["properties"]["Name"]["title"][0]["plain_text"]
        workout_ex_sets = workout_ex_db[n]["properties"]["Sets"]["number"]
        workout_ex_reps = workout_ex_db[n]["properties"]["Reps"]["number"]
        workout_ex_weight = workout_ex_db[n]["properties"]["Weight"]["number"]
        workout_ex_data = { 
                            "name" : workout_ex_name,
                            "sets" : workout_ex_sets,
                            "reps" : workout_ex_reps,
                            "weight" : workout_ex_weight,
                        }

        workout_exercises.append(workout_ex_data)

    return workout_exercises


def data_formatter(workout : dict):
    """
    Formats the workout data and the exercise data to a more legible structure.
    For a given workout, returns a formated workout data dictionary.
    """

    workout_date = workout["properties"]["Date"]["date"]["start"]
    workout_intensity = workout["properties"]["Intensity"]["select"]["name"]
    workout_location = workout["properties"]["Location"]["select"]["name"]
    workout_duration = workout["properties"]["Duration"]["number"]

    # Format the exercise data
    exercise_data = exercise_formatter(workout)

    return { 
            "date" : workout_date,
            "intensity" : workout_intensity,
            "location" : workout_location,
            "duration" : workout_duration,
            "exercises" : exercise_data
            }



def preprocess():
    """
    Data preprocessing pipeline.
    The result is a JSON file with the data in the desired structure.
    """

    # 1. Get the data from Notion database.
    wts_db_data = get_notion_data()
    
    # 2. Format it to the desired structure 
    data = []
    for workout in wts_db_data:
        data.append(data_formatter(workout))

    print("Succesfully workouts data generated.")

    # 3. Save the data to a JSON file
    # FIXME: Does this create the directory if it doesn't alredy exist?
    with open("./data/workouts_data.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    # Define TOKEN and DATABASE_ID
    load_dotenv()
    config = dotenv_values("./.env/.env") 
    NOTION_TOKEN = config["NOTION_TOKEN"]
    DATABASE_ID = "3badcbc40d434e00835bd09930f4a801"

    HEADERS = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # Run the preprocessing pipeline
    preprocess()

    # FIXME: What if the data coming doesn't have the wokrout-exercise structure?