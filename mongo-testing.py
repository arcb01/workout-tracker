import json
from pymongo import MongoClient
import pprint

# Connect to MongoDB
client = MongoClient('mongodb://192.168.0.32:2717/')
db = client['gym']


def create_collection(collection_name : str):
    """
    Creates a collection in the database and applies a validation schema to it.
    NOTE: The validation schema is read from a json file with the same name as the collection.
    """

    # Create collection
    try:
        db.create_collection(collection_name)
    except:
        print(f"Collection {collection_name} already exist")

    # Read validation schema
    try:
        with open(f"./data/{collection_name}_validation_schema.json", "r") as f:
            validation_schema = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Make sure the collection name has the same name as the json file: {collection_name} == {collection_name}_validation_schema.json")

    # Apply validation schema
    try:
        db.command({"collMod": collection_name, "validator": validation_schema})
    except:
        print("Validator already exist")


def show_validation_schema(collection_name : str):
    """
    Prints the validation schema of a collection.
    """

    validation_info = db[collection_name].options()["validator"]

    pprint.pprint(validation_info)

# Create collections
create_collection("exs")
create_collection("wsns")

# Show validation schema
show_validation_schema("exs")

# Read data from json file
with open("./data/w_data.json", "r") as f:
    data = json.load(f)
    exs_data = data["exercises"]
    wsns_data = data["workout_sessions"]

# Insert exercises data to collection
exs_ids = db["exs"].insert_many(exs_data).inserted_ids

# Insert workout sessions data to collection
# TODO: Prepro
for workout in wsns_data:
    workout["exercises"] = [ for ex in workout["exercises"]]
wsns_ids = db["wsns"].insert_many(wsns_data).inserted_ids

client.close()
