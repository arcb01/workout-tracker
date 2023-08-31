import json
import pprint

def create_collection(db: object, collection_name : str):
    """
    Creates a collection in the database and applies a validation schema to it.
    """

    # Create collection
    try:
        db.create_collection(collection_name)
        print("Collection created succesfully""")
    except:
        print(f"Collection {collection_name} already exist")

def apply_validation_schema(db: object, collection_name : str):
    # Read validation schema
    try:
        with open(f"./data/val_schemas/{collection_name}_val_schema.json", "r") as f:
            validation_schema = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Make sure the collection name has the same name as the json file: {collection_name} == {collection_name}_val_schema.json")

    # Apply validation schema
    try:
        # Delete validation schema if already exist
        db.command({"collMod": collection_name, "validator": {}})
        db.command({"collMod": collection_name, "validator": validation_schema})
        print("Validation schema applied succesfully")
    except Exception as e:
        print(e)

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
    """
    Shows all the documents in a collection.
    """
    all_documents = collection.find()

    for document in all_documents:
        pprint.pprint(document)