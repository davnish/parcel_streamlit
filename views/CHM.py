import streamlit as st
from main import base
from streamlit_timeline import st_timeline
import os
import glob

class chm_map(base):
    def __init__(self, title_name, color_column, popup, aliases, colormap=None, legend_order=None):
        super().__init__(title_name, color_column, popup, aliases, colormap, legend_order)

    def get_path(self):
        # Making selectbox
        c1, c2, c3, c4 = st.columns(4)

        with c1: state = st.selectbox("Select your State:", ['Madhya Pradesh', 'Uttar Pradesh','Haryana'])
        year = []

        if state == 'Madhya Pradesh':
            district = ['Vidisha']
            village = ['Bhaumrasa'] # !Need to change this
            year.extend(['2024'])

        elif state == 'Uttar Pradesh':
            district = ['Mathura']
            village = ['Nagla Dhanoua']
            year.extend(['2022', '2023','2024'])

        else:
            district = ['Bhiwani']
            village = ['Ajitpur'] # !Need to change this
            year.extend(['2022', '2023','2024'])


        with c2: district = st.selectbox("Select your District:", district)
        with c3: village = st.selectbox("Select your Village:", village)
        with c4: year = st.selectbox("Select your Year", year)

        path = None

        path = r"chm"
        if district == 'Mathura':
            path = os.path.join(path, 'mathura', year)
        elif district == 'Bhiwani':
            path = os.path.join(path, 'bhiwani', year)
        elif district == 'Vidisha':
            path = os.path.join(path, 'vidisha', year)


        # items = [{'id': idx, 'content': os.path.splitext(os.path.split(date)[1])[0], 'start': os.path.splitext(os.path.split(date)[1])[0]} for idx, date in enumerate(glob.glob(os.path.join(path, "*.gpkg")))]
        items = [{'id': idx, 'content': os.path.splitext(os.path.split(date)[1])[0], 'start': os.path.splitext(os.path.split(date)[1])[0]} for idx, date in enumerate(glob.glob(os.path.join(path, "*.shp")))]

        timeline = st_timeline(items, groups=[], options={}, height="200px")

        if timeline:
            path = os.path.join(path, f'{timeline["start"]}.shp')
        else: 
            path = None



        return path
    
    def __call__(self):
        path = self.get_path()
        self.set_map()

        if path:
            # Making visualization of the village
            self.add_parcel_map(path)

        self.m.to_streamlit(layout = 'wide')
    
    # def add_parcel_map(self, path):
    #     # self.gdf['res'] = self.gdf[color_column].apply(lambda x: 'Low' if x <= 0.3 else ('Healthy' if x > 0.55 else 'Moderate'))
    #     self.color_column = 'Category'
    #     return super().add_parcel_map(path)


                
title_name = 'Crop Health Monitoring'
colormap = None
color_column = 'Category'
popup = ['mean']
aliases = ['Mean']
legend_order = ['High', 'Moderate', 'Low']
chm_map(title_name, color_column, popup, aliases, colormap=colormap, legend_order = legend_order)()



