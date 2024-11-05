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

        with c1: state = st.selectbox("Select your State:", ['Madhya Pradesh'])

        if state == 'Madhya Pradesh':
            district = ['Vidisha']
            village = ['Bhaumrasa'] # !Need to change this

        elif state == 'Uttar Pradesh':
            district = ['Mathura']
            village = ['Nagla Dhanoua']
        else:
            district = ['Bhiwani']
            village = ['Ajitpur'] # !Need to change this

        with c2: district = st.selectbox("Select your District:", district)
        with c3: village = st.selectbox("Select your Village:", village)
        with c4: year = st.selectbox("Select your Year", ["2024"])
        # with c5: date = st.selectbox("Select your Date", ["25_June", "09_June", "11 July", "12_August", "28 August", "13 September", ])

        # search = st.button('Get Map')
        # if search: st.session_state['button_clicked'] = True
        path = None

        path = r"chm"
        if district == 'Mathura':
            path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
        elif district == 'Bhiwani':
            path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
        else:
            path = os.path.join(path, 'vidisha')


        items = [{'id': idx, 'content': os.path.splitext(os.path.split(date)[1])[0], 'start': os.path.splitext(os.path.split(date)[1])[0]} for idx, date in enumerate(glob.glob(os.path.join(path, "*.gpkg")))]

        timeline = st_timeline(items, groups=[], options={}, height="200px")

        # search = st.button('Get Map')
        # if search: st.session_state['button_clicked'] = True

        if timeline:
            path = os.path.join(path, f'{timeline["start"]}.gpkg')
        else: 
            path = None

        # st.subheader("Selected item")
        # st.write(timeline["start"])

        return path
    
    def __call__(self):
        path = self.get_path()

        if path is not None:
        # Making visualization of the village
            self.get_map(path)
    
    def add_parcel_map(self):
        self.gdf['res'] = self.gdf[color_column].apply(lambda x: 'Low' if x <= 0.3 else ('Healthy' if x > 0.55 else 'Moderate'))
        self.color_column = 'res'
        return super().add_parcel_map()


                
title_name = 'Crop Health Monitoring'
colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = '_mean'
popup = ['_mean']
aliases = ['Mean']
legend_order = ['Healthy', 'Moderate', 'Low']
chm_map(title_name, color_column, popup, aliases, colormap=colormap, legend_order = legend_order)()



