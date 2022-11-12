from notion_api import read_database, read_page
from workout_class import Workout
import pprint, json
import pandas as pd
import pickle


def workout_data(headers, database_id):
    """ Returns a list of Workout objects """

    print("\nRetrieving data from API...\n")
    # Read database
    db_name = "db"
    read_database(db_name, database_id, headers)
    wkrts_objs = []

    # Open db json
    with open(f"./data/{db_name}.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        pages = data["results"]

        # For every page in the workout db, append to list a Workout object
        # with its main properties
        for page in pages:
            wrkt_satus = page["properties"]["Status"]["status"]["name"]
            wrkt_date = pd.to_datetime(page["properties"]["Date"]["date"]["start"])
            wrkt_name = page["properties"]["Name"]["title"][0]["text"]["content"] # 0 is OK
            page_id = page["id"]
            w = Workout(wrkt_name, wrkt_date, wrkt_satus, page_id)
            wkrts_objs.append(w)

        # For every page (inside)
        for i in range(len(wkrts_objs)):
            wrkt_id = wkrts_objs[i].id
            wrkt_name = wkrts_objs[i].name
            read_page(wrkt_id, wrkt_name, headers)
            # Open every page and read its inner_db content
            with open(f"./data/pages/page_{wrkt_name}.json", encoding="utf8") as json_pg_file:
                data2 = json.load(json_pg_file)
                # FIXME: maybe check before that its child database is == "session"?
                workout_db_id = data2["results"][0]["id"]
                read_database("inner_db", workout_db_id, headers)
                # Transform inner_db to dataframe
                with open(f"./data/inner_db.json", encoding="utf8") as json_db_file:
                    data3 = json.load(json_db_file)
                    wkrt_db = data3["results"]
                    df_data = {"Exercise" : [], "Sets & Reps" : []}
                    for row in wkrt_db:
                        if row["properties"]["Sets & Reps"]["rich_text"]:
                            sets_n_reps = (row["properties"]["Sets & Reps"]["rich_text"][0]["text"]["content"] # 0 is OK
                                            .strip(" ")
                                            .split()) 
                            exercise = row["properties"]["Exercise"]["title"][0]["text"]["content"] # 0 is OK
                            df_data["Exercise"].append(exercise)
                            df_data["Sets & Reps"].append(sets_n_reps)
                        
                    wrkt_df = pd.DataFrame.from_dict(df_data)
                    wkrts_objs[i].wrkt_df = wrkt_df

    # NOTE: Elements inside the list are REVERSED
    list_of_wrkts = wkrts_objs

    with open('./data/workout_objects.pickle', 'wb') as handle:
        pickle.dump(list_of_wrkts, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n Succesful retrieval!\n")

