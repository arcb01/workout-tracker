import json
import pprint

def create_collection(db: object, collection_name : str):
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
    """
    try:
        with open(f"./data/val_schemas/{collection_name}_val_schema.json", "r") as f:
            validation_schema = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Make sure the collection name has the same name as the json file: {collection_name} == {collection_name}_val_schema.json")

    # Apply validation schema
    try:
        db.command({"collMod": collection_name, "validator": validation_schema})
    except:
        print("Validator already exist")
    """

def show_validation_schema(db: object, collection_name : str):
    """
    Prints the validation schema of a collection.
    """

    validation_info = db[collection_name].options()["validator"]

    pprint.pprint(validation_info)

def delete_collection_data(db: object, collection_name : str):
    """
    Deletes all the data in a collection.
    """

    try:
        db[collection_name].delete_many({})
    except:
        print("Collection already empty")

def delete_collection(db: object, collection_name : str):
    """
    Deletes a collection.
    """

    try:
        db[collection_name].drop()
    except:
        print("Collection already deleted")

def show_collection(collection : object):
    all_documents = collection.find()

    for document in all_documents:
        pprint.pprint(document)

def empty_database(db : object):
    """
    Deletes all the data in the database.
    """

    for collection in db.list_collection_names():
        delete_collection_data(db, collection)
