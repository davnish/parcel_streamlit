import pandas as pd
import streamlit as st
from main import base
import os


class weather_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path, color_dict):
        super().__init__(title_name, color_column, popup, aliases, path, color_dict=color_dict)

    def get_path(self):
        # Making selectbox

        parameter = []
        # print(self.path)
        if self.year: parameter = self.get_options_dir(self.path)
        self.parameter = st.selectbox("Select your parameter", parameter, index = None, placeholder='Select')

        if self.parameter: 
            self.path = os.path.join(self.path, self.parameter.lower())
            self.path =  self.get_filename()
        
        # return self.path

    def __call__(self):
        self.format()
        self.get_path()

        if self.parameter:
        # Making visualization of the village
            self.add_parcel_map(self.path)
        self.m.to_streamlit(layout = 'wide')
        # return self.year


title_name = 'Weather Data'
path = r'data/weather'
color_column = 'cate'
popup = ['Khasra_No']
aliases = ['Khasra No:']
# title_name = 'Crop Map'
color_dict = {'1 - 1.5 mm': 'blue', '1.5 - 2 mm': 'orange'}
weather_map(title_name, color_column, popup, aliases, path, color_dict=color_dict)()

if base.get_key_value('year') == '2022':
    df = pd.read_csv(r'data/weather/Ajeetpur_precip_time_series.csv')
    # df = df[]
    df = df[20: 41]
    df['validdate'] = df['validdate'].str.slice(0, 10)
    df['Precipitation'] = df['precip_24h:mm']
    st.line_chart(df, x='validdate', y="Precipitation")