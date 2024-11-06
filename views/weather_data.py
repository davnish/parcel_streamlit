import pandas as pd
import streamlit as st
# import leafmap.foliumap as leafmap
import geopandas as gpd
from main import base
import os
st.set_page_config(layout="wide")

class weather_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path, color_dict):
        super().__init__(title_name, color_column, popup, aliases, path, color_dict=color_dict)

    def get_path(self):
        # Making selectbox

        parameter = []
        print(self.path)
        if self.year: parameter = self.get_options_dir(self.path)
        self.parameter = st.selectbox("Select your parameter", parameter, index = None, placeholder='Select')

        if self.parameter: 
            self.path = os.path.join(self.path, self.parameter.lower())
            self.path =  self.get_filename()
        
        return self.path

    def __call__(self):
        self.format()
        path = self.get_path()

        if path and self.parameter:
        # Making visualization of the village
            self.add_parcel_map(path)
        self.m.to_streamlit(layout = 'wide')
        return self.year





title_name = 'Weather Data'
path = r'data/weather'
color_column = 'cate'
popup = ['Khasra_No']
aliases = ['Khasra No:']
# title_name = 'Crop Map'
color_dict = {'1 - 1.5 mm': 'blue', '1.5 - 2 mm': 'orange'}
tillage = weather_map(title_name, color_column, popup, aliases, path, color_dict=color_dict)()

if tillage == '2022':
    df = pd.read_csv(r'data/weather/Ajeetpur_precip_time_series.csv')
    df['Precipitation'] = df['precip_24h:mm']

    st.line_chart(df, x='validdate', y="Precipitation")