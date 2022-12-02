#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import seaborn as sns
import pickle
import datetime
import plotly.graph_objects as go
from ipywidgets import widgets
from workout_class import Workout

# # Data preprocessing
# ---

# Load files

# In[2]:

import os 
with open('./data/workout_objects.pickle', 'rb') as handle:
    wrkts_list = pickle.load(handle)


# Load a csv files that contains every workout date

# In[3]:


dic = {"Name" : [], "Date" : [], "Status" : []}

for w_obj in wrkts_list:
    dic["Name"].append(w_obj.name)
    dic["Date"].append(w_obj.date)
    dic["Status"].append(w_obj.status)
    
all_wrkts_df = (pd.DataFrame.from_dict(dic)
                    .sort_values(by=['Date'])
                    .reset_index(drop=True))
all_wrkts_df['Date'] = pd.to_datetime(all_wrkts_df['Date'], infer_datetime_format=True)


# ## Adding total volume

# In[4]:


str_to_int = lambda l : [int(el) for el in l]

def calc_total_volume(l : list, wrkt_status : str):
    """ 
    Formula for calculating total volume for every exercise
    total_volume = sum(reps in all sets) * penalization
    """
    
    penalization_dic = {
        "Done" : 1.0, # No penalization
        "At home" : 0.7,
        "Mini" : 0.5,
    }
    
    value = sum(l)
    total_volume = value * penalization_dic[wrkt_status] 
    
    return float(total_volume)


# **Calculate total volume for every done workout session**

# In[5]:


# Done workouts
done = ["Mini", "Done", "At home"]

# For every workout object, pick its df and 
# if its not empty and status is done, calculate total volume
# NOTE: total volume for Testing workouts is not calculated (NaN)
for w_obj in wrkts_list:
    w_df = w_obj.wrkt_df
    total_volume_col = np.array([])
    for i, r in w_df.iterrows():
        if (type(r["Sets & Reps"]) == list) and (w_obj.status in done):
            sets_n_reps = str_to_int(r["Sets & Reps"])
            total_volume = calc_total_volume(sets_n_reps, w_obj.status)
            total_volume_col = np.append(total_volume_col, total_volume)
    w_df["total_volume"] = pd.Series(total_volume_col)


# # Data analysis
# ---

# ## Functions

# ### Workout frequency

# Per cada tipus de workout, calcula quina es la seva frenquencia sobre el nombre total de wokrouts

# In[6]:


def workout_freq(df):
    """
    Returns which type of workout is more frequent (in percentage)
    """
    
    res = {}
    total_n_wouts = sum(df["Status"].value_counts())
    d = df["Status"].value_counts().to_dict() # Dict with all the occurrences
    #print(f"\n === Total number of workouts is {total_n_wouts} ===\n")
    
    # Calculate the percentage for every workout
    for w_type, n in d.items():
        percentage = round((n / total_n_wouts) * 100, 2)
        #print(f"{w_type} - {percentage}%")
        res[w_type] = percentage
        
        
    df = pd.DataFrame({'Type of workout' : list(res.keys()), 
                     'Frequency' : list(res.values())})
        
        
    return df


# ### Workout consistency
# 

# Per cada mes, calcula la consistency a partir del numero de workouts

# Consistency should be **>= 80 %**

# In[7]:


from collections import Counter

def consistency(df, total=False):
    """
    Calculates the consistency of workouts for every month. 
    It also calculates the average consistency across all months. (currently unused)
    Returns a dataframe
    """
    
    min_n_wouts_per_month = 13
    df = df[ ~df["Status"].isin(["Testing", "Failed"])] # Only take into acount "Completed" workouts
    months_freq_wrkt = [d.month for d in df["Date"]]
    months = list(set(months_freq_wrkt)) # List containing only the month of every wokrout
    workouts_per_month = Counter(months_freq_wrkt) # Count the number of workouts per mmonth
    workouts_consistency_per_month = dict(workouts_per_month.copy())

    # Dictionary with the consistency of each month
    for month, n in workouts_per_month.items():
        month_freq = n / min_n_wouts_per_month
        workouts_consistency_per_month[month] = round(month_freq * 100, 2)
        
    # Averages consistency across all months
    overall_consistency = sum(workouts_consistency_per_month.values()) /                             len(workouts_consistency_per_month)
    
    #print("\n=== Consistency for each month (%) ===\n")
    #pretty(workouts_consistency_per_month, 0)
    #print(f"\n=== Overall consistency (%) ===\n {overall_consistency} \n")
    
    # if True all consistency values will be 100 (for graphing pourposes)
    if total:
        consistency = [100] * len(list(workouts_consistency_per_month.keys()))
    else:
        consistency = list(workouts_consistency_per_month.values())
    
    df = pd.DataFrame({'Month' : list(workouts_consistency_per_month.keys()), 
                     'Consistency' : consistency})
    
    return df
    


# In[8]:


df_consistency = consistency(all_wrkts_df)


# ### Workout perforamnce

# Tracks each exercise performance for every month 

# In[9]:


# Group workout dfs by month
dic_months = {wrkt["Date"].month : [] for i, wrkt in all_wrkts_df.iterrows()}

for w_obj in wrkts_list:
    w_df = w_obj.wrkt_df
    w_date = w_obj.date.month
    dic_months[w_date].append(w_df)
    
# Group every workout df by month and calculate an avg of the total_volume
# {9 : september_goruped_df, 10 : october_goruped_df, ...}
dic_grouped_df_month = { month : (pd.concat(obj_list)
                                  .groupby('Exercise')
                                  .agg({'total_volume': 'mean'}))
                                .reset_index()
                                for month, obj_list in dic_months.items()
                        }


# **Performance by month of every exercise**

# In[10]:


list_exercises = list(dic_grouped_df_month[9]["Exercise"])
months = list(dic_grouped_df_month.keys())


# In[11]:


# Dictionary for converting num month to str
map_month = {1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr",
                5 : "May", 6 : "Jun", 7 : "Jul", 8 : "Aug",  
                9 : "Sep", 10 : "Oct", 11 : "Nov",  12 : "Dec"}

# Function that converts num months to string
num_to_month = lambda l : [map_month[num_month] for num_month in l]


# In[12]:


res = []

for ex in list_exercises:
    for m in list(map_month.keys()):
        try:
            month_df = dic_grouped_df_month[m]
            ex_value = month_df[month_df["Exercise"] == ex]["total_volume"].values[0]
        except:
            ex_value = 0.0
        res.append((ex, map_month[m], ex_value))

# DF showing performance for every exercise by month
df_ex_perf = pd.DataFrame(res,
                      columns =['Exercise', 'Month', 'Performance'])


# In[13]:


freq_dict = all_wrkts_df["Status"].value_counts().to_dict()
names = list(freq_dict.keys())
total_n_wouts = sum(list(freq_dict.values()))
freqs = list(map(lambda f : round(f / total_n_wouts * 100, 2), 
         list(freq_dict.values())))


# In[14]:


df_wrkt_freq = pd.DataFrame(list(zip(names, freqs)), 
                            columns =['Type of workout', 'Frequency'])


def avg_wrkt_sets_per_week(df, exercise):
    """
    Returns a dataframe with the average number of sets 
    per week for a given exercise
    """

    n_wrkouts = df.shape[0]
    avg_sets_per_week = lambda n_sets : (n_sets  / n_wrkouts) * 4
    dic_sets = {ex : 0 for ex in list_exercises}
    for ex in list_exercises:
        for w_obj in wrkts_list:
            w_df = w_obj.wrkt_df
            if not w_df.empty and ex in w_df["Exercise"].values:
                n_sets = len(w_df[w_df["Exercise"] == ex]["Sets & Reps"].values[0])
                dic_sets[ex] += n_sets

    dic_avg_sets_per_week = {ex : round(avg_sets_per_week(total_n_sets), 2)
                                for ex, total_n_sets in dic_sets.items()}
    
    # convert dict to df
    df_avg_sets_per_week = pd.DataFrame.from_dict({"Exercise" : list(dic_avg_sets_per_week.keys()), 
                            "AVG" : list(dic_avg_sets_per_week.values())}, orient='columns')

    return df_avg_sets_per_week


df_avg_wrkt_sets_per_week = avg_wrkt_sets_per_week(all_wrkts_df, "Dips")

# # Saving

# In[15]:


# DF showing frequency for every workout type
df_wrkt_freq.to_csv('./data/processed/workout_freq.csv')

# DF showing overall workout consistency by month
df_consistency.to_csv('./data/processed/workout_consistency.csv')

# DF showing performance for every exercise by month
df_ex_perf.to_csv('./data/processed/workout_performance.csv')

# DF showing average number of sets per week for every exercise
df_avg_wrkt_sets_per_week.to_csv("./data/processed/avg_wrkt_sets_per_week.csv")