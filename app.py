from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    # Show dashboard
    show_dashboard()
    return {"Hello": "World"}

def show_dashboard():
    # 1. Update the database
    update_database()
    # 2. Query the data from the database to form a plot (csv foramt)
    get_plot_data()
    # 4. Show the plot
    show_plot()
