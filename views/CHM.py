import streamlit as st
from main import base
from streamlit_timeline import st_timeline
import os
import glob
st.set_page_config(layout="wide")

class chm_map(base):
    def __init__(self, title_name, color_column, popup, aliases, legend_order=None):
        super().__init__(title_name, color_column, popup, aliases, legend_order)

    def get_path(self):
        # Making selectbox

        path = None
        path = r"chm"
        if self.district == 'Mathura' and self.year:
            path = os.path.join(path, 'mathura', self.year)
        elif self.district == 'Bhiwani' and self.year:
            path = os.path.join(path, 'bhiwani', self.year)
        elif self.district == 'Vidisha' and self.year:
            path = os.path.join(path, 'vidisha', self.year)


        items = [{'id': idx, 'content': os.path.splitext(os.path.split(date)[1])[0], 'start': os.path.splitext(os.path.split(date)[1])[0]} for idx, date in enumerate(glob.glob(os.path.join(path, "*.shp")))]

        timeline = st_timeline(items, groups=[], options={}, height="200px")

        if timeline:
            path = os.path.join(path, f'{timeline["start"]}.shp')
        else: 
            path = None
        return path
    
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
# colormap = None
color_column = 'Category'
popup = ['mean']
aliases = ['Mean']
legend_order = ['High', 'Moderate', 'Low']
chm_map(title_name, color_column, popup, aliases, legend_order = legend_order)()



