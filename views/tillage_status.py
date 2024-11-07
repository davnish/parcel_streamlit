import pandas as pd
import streamlit as st
from main import base


st.set_page_config(layout="wide")

class sowing_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path, legend_order, color_dict):
        super().__init__(title_name, color_column, popup, aliases, path, legend_order=legend_order, color_dict=color_dict)

    def get_path(self):
        if self.year: self.path = self.get_filename()
        return self.path
    
    def add_parcel_map(self, path):
        self.color_column = self.year + '_Max'
        return super().add_parcel_map(path)

    def __call__(self):
        self.format()
        path = self.get_path()
        if path and self.year:
            # Making visualization of the village
            self.add_parcel_map(path)
        self.m.to_streamlit(layout = 'wide')



title_name = 'Tillage Status'
path = r'data/tillage'
color_column = None
popup = None
aliases = None
color_dict = {'02-07-2022': 'red', '16-06-2022': 'green', '18-07-2022': 'blue', 
              '05-06-2024': 'red',  '23-07-2024':'green', }
legend_order = ['16-06-2022', '02-07-2022', '18-07-2022']
sowing_map(title_name, color_column, popup, aliases, path, legend_order = legend_order, color_dict = color_dict)()
