import streamlit as st
from main import base
from streamlit_timeline import st_timeline
import os
import glob
import pandas as pd
st.set_page_config(layout="wide")

class chm_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path, legend_order):
        super().__init__(title_name, color_column, popup, aliases, path, legend_order=legend_order)

    def get_path(self):

        items = [{'id': idx, 'content': os.path.splitext(os.path.split(date)[1])[0], 'start': os.path.splitext(os.path.split(date)[1])[0]} for idx, date in enumerate(glob.glob(os.path.join(self.path, "*.shp")))]
        timeline = st_timeline(items, groups=[], options={}, height="200px")

        if timeline:
            self.path = os.path.join(self.path, f'{timeline["start"]}.shp')
        else: 
            self.path = None

        return self.path
    
    def __call__(self):
        self.format()
        path = self.get_path()

        if path:
            # Making visualization of the village
            self.add_parcel_map(path)

        self.m.to_streamlit(layout = 'wide')

                
title_name = 'Crop Health Monitoring'
path = r'data/chm'
# colormap = None
color_column = 'Category'
popup = ['mean']
aliases = ['Mean']
legend_order = ['High', 'Moderate', 'Low']
chm_map(title_name, color_column, popup, aliases, path, legend_order = legend_order)()

chm_year = base.get_key_value('year')
chm_state = base.get_key_value('state')
if chm_year == '2024':
    path = os.path.join(path, chm_state.lower(), chm_year, 'chart')
    filename = [i for i in os.listdir(path) if i.endswith('.csv')][0]
    df = pd.read_csv(os.path.join(path, filename), index_col = None)
    df['image_date'] = df['image_date'].str.slice(0, 10)
    st.line_chart(df, x='image_date')



