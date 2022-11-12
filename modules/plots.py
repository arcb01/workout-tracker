import pandas as pd
import plotly.graph_objects as go
from ipywidgets import widgets
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def donut_chart(data):
    labels = list(data["Type of workout"].values)
    values = list(data["Frequency"].values)
    
    colors =  ['rgb(218, 44, 56)', 'rgb(34, 111, 84)', 'rgb(135, 195, 143)', 'rgb(244, 240, 187)']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
    fig.update_layout(width=800,
                        height=600)

    return fig


def bar_chart(data, ex):

    filter_list = data["Exercise"] == ex
    temp_df = data[filter_list]
    x1 = temp_df['Month']
    x2 = temp_df['Performance']

    trace1 = go.Figure([go.Bar(x=x1, y=x2,
                          marker=dict(color="rgba(82, 84, 102, 0.65)",
                               line=dict(color="rgba(82, 84, 102, 1.0)", width=1.75)))
             ])
        
             
    trace1.update_layout(height=500,width=800,
                        xaxis_title="Month", yaxis_title="Total volume")

    #trace1.update_traces(marker_color='#2b2d42', opacity=.8)

    g = go.FigureWidget(data=trace1,
                        layout=go.Layout(
                            barmode='overlay'
                        ))

    return g


def progress_bar_chart(data):

    # For graphing pourposes, we need totals out of 100
    df_total_vis = data.copy()
    df_total_vis["Consistency"] = 100
    total_consistency = df_total_vis

    fig = go.Figure()
    fig.add_trace( go.Bar(
                        name = "Consistnecy",
                        x = data["Consistency"],
                        y = data["Month"],
                        orientation = 'h',
                        marker=dict(color="rgba(53, 143, 128, 1.0)",
                                line=dict(color="rgba(3, 102, 102, 1.0)", width=1.75)))
                )

    fig.add_trace( go.Bar(
                    x=total_consistency["Consistency"],
                    y=total_consistency["Month"],
                    orientation='h', 
                    showlegend = False,
                    marker=dict(color="rgba(53, 143, 128, .10)")
                                #line=dict(color="rgba(0, 0, 0, 1.0)", width=1.75)))
                ))

    fig.add_vline(x=80, line_width=1.5, line_dash="dash", line_color="rgba(3, 102, 102, .8)")
                
    fig.update_layout(barmode='stack',
                        title="Workout consisntecy per month",
                        width=1100,
                        height=300,
                        xaxis_title="Consistency (%)",
                        yaxis_title="Month")
    fig.update_xaxes(range = [0,100])

    return fig