import os

file1 = "./modules/run_retriever.py"
file2 = "./modules/data_processing.py"
file3 = "./workout_dashboard.py"

os.system(f'python {file1}')
os.system(f'python {file2}')
os.system(f'streamlit run {file3}')

