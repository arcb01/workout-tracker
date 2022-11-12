@echo off
python "D:\V\Projects\Python\Data Analysis\Notion gym workout\dashboard-v3\modules\run_retriever.py"
python "D:\V\Projects\Python\Data Analysis\Notion gym workout\dashboard-v3\modules\data_processing.py"
streamlit run "D:\V\Projects\Python\Data Analysis\Notion gym workout\dashboard-v3\workout_dashboard.py"
pause