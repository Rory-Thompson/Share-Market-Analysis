import plotly.graph_objects as go
from dash import dcc, html
import importlib
from dash import Dash
import pandas as pd
import matplotlib.pyplot as plt
import Dashboard_testing.layout

# Now re-import the class and test again
importlib.reload(Dashboard_testing.layout)
from Dashboard_testing.layout import create_layout



class Dashboard_creator:

    def __init__(self,codes,Plotter):
        #self.SharesPlotter = SharesPlotter
        self.codes = codes
        self.app = Dash()
        self.app.title = "Shares Analyis"
        print(f"codes passed into layout from dashboard { self.codes}")
        self.app.layout = create_layout(self.app,codes = self.codes,Plotter = Plotter)
        #self.app.run()
        
    def run(self, host="0.0.0.0", port=8050, debug=True):
        """Starts the Dash app."""
        self.app.run(host=host, port=port, debug=debug,use_reloader=False)
        #initial instantiation of the app, maybe should be seperate method? 
        

    #@property
    #def SharesPlotter(self):#not useful, would have to create a method for everything
        #return self.SharesPlotter

    





