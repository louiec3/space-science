import pandas as df
import plotly.express as px
import plotly.graph_objects as go

def trace_orbit(fig, df, orbit_name):
    trace = fig.add_scatter(
                x=df['X'], 
                y=df['Y'], 
                name=orbit_name
            )
    
    return trace