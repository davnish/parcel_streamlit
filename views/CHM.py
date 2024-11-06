import streamlit as st
from main import base
from streamlit_timeline import st_timeline
import os
import glob
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
    
    # def add_parcel_map(self, path):
    #     # self.gdf['res'] = self.gdf[color_column].apply(lambda x: 'Low' if x <= 0.3 else ('Healthy' if x > 0.55 else 'Moderate'))
    #     self.color_column = 'Category'
    #     return super().add_parcel_map(path)


                
title_name = 'Crop Health Monitoring'
path = r'data/chm'
# colormap = None
color_column = 'Category'
popup = ['mean']
aliases = ['Mean']
legend_order = ['High', 'Moderate', 'Low']
chm_map(title_name, color_column, popup, aliases, path, legend_order = legend_order)()



