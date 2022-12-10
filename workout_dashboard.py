import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.plots import *
import time

#path = r"D:\V\Projects\Python\Data Analysis\Notion gym workout\dashboard-v3\workout-tracker"

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header('Workout dashboard')

# Row B
workout_freq = pd.read_csv('./data/processed/workout_freq.csv')
workout_perf = pd.read_csv('./data/processed/workout_performance.csv')
workout_consist = pd.read_csv('./data/processed/workout_consistency.csv')
avg_weekly_n_sets = pd.read_csv('./data/processed/avg_wrkt_sets_per_week.csv')

c1, c2 = st.columns((7,3)) # Columns


with c1:
    st.markdown('### Exercise performance')
    # Create select box for filtering data before plotting
    exercise = st.selectbox('Select exercise', options=workout_perf["Exercise"].unique())
    avg_n_sets_ex = avg_weekly_n_sets[avg_weekly_n_sets["Exercise"] == exercise]["AVG"].values[0]
    st.write(f'Average number of sets in the last week = **{avg_n_sets_ex}**')
    # PLot bar chart
    plot = bar_chart(workout_perf, exercise)
    st.plotly_chart(plot, use_container_width=True)
with c2:
    st.markdown('### Workout status frequency')
    # Plot donut chart
    fig = donut_chart(workout_freq)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('### Consistency')
prog_fig = progress_bar_chart(workout_consist)
st.plotly_chart(prog_fig)