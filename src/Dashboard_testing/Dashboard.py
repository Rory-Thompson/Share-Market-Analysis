import plotly.graph_objects as go
from dash import dcc, html
import importlib
from dash import Dash
import pandas as pd
import matplotlib.pyplot as plt
import layout

# Now re-import the class and test again
importlib.reload(layout)
from layout import create_layout



class Dashboard_creator:

    def __init__(self,codes):
        #self.SharesPlotter = SharesPlotter
        self.codes = codes
        self.app = Dash()
        self.app.title = "Penis"
        self.app.layout = create_layout(self.app,codes = self.codes)
        self.app.run()
        
        
        #initial instantiation of the app, maybe should be seperate method? 
        

    #@property
    #def SharesPlotter(self):#not useful, would have to create a method for everything
        #return self.SharesPlotter

    





