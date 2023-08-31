from fastapi import FastAPI
from mongo_handler import update_db, get_plot_data

app = FastAPI()

@app.get("/")
def read_root():
    return show_dashboard()

def show_dashboard():
    # 1. Run the update_db function in sync mode
    update_db()
    # 2. Query the data from the database to form a plot (csv foramt)
    data = get_plot_data()
    # 3. TODO: Show the plot in the browser
    return data