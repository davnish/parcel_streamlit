import streamlit as st
from main import base
import os

class yield_map(base):
    def __init__(self, title_name, color_column, popup, aliases, colormap=None):
        super().__init__(title_name, color_column, popup, aliases, colormap)

    def get_path(self):
        # Making selectbox
        c1, c2, c3, c4 = st.columns(4)
        c5, c6, c7,c8 = st.columns(4)
        c9, c10, c11, c12 = st.columns(4)

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
        with c3: block = st.selectbox("Select Block: ",[231, 234, 1])
        with c4: IU = st.selectbox("Select IU: ",[231, 234, 1])
        with c5: village = st.selectbox("Select your Village:", village)
        with c6: year = st.selectbox("Select your Year", ["2022", "2024"])
        with c7: crop_type = st.selectbox("Select your Crop", ["Soybean"])
        with c8: khasrano = st.selectbox("Select Khasra No: ",[231, 234, 1])
        with c9: Season = st.selectbox("Select Season: ",[231, 234, 1])
        with c10: indices = st.selectbox("Select your Indices: ",["NDVI", "EVI"])
        with c11: npk_soilmap = st.radio("Select your type: ",["Soil Map", "NPK"])
        # with c12: indices = st.("Select your Indices: ",["NDVI", "EVI"])


        search = st.button('Get Map')
        if search: st.session_state['button_clicked'] = True
        path = None
        if st.session_state['button_clicked']:
            path = r"yield"
            if district == 'Mathura':
                path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
            elif district == 'Bhiwani':
                path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
            else:
                path = os.path.join(path, 'vidisha')
                if year == '2022':
                    path = os.path.join(path,'2022', "2022_ZONAL.shp")
                else:
                    path = os.path.join(path, '2024', "2024_ZONALL.shp")
        return path
    
    def __call__(self):
        path = self.get_path()

        if path is not None:
        # Making visualization of the village
            self.get_map(path)
                
title_name = 'Crop Health Monitoring'
colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = 'yie_cate'
popup = ['yie_cate', 'y(kg/ha)']
aliases = ['Yield Category:', 'Yield (Kg/Hec):']

yield_map(title_name, color_column, popup, aliases, colormap=colormap)()
