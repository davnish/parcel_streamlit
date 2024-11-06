import streamlit as st
from streamlit_folium import st_folium
import os
from main import base

st.set_page_config(layout="wide")

class claims_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path):
        super().__init__(title_name, color_column, popup, aliases, path)

    def get_path(self):
        crops = []
        if self.year: crops.extend(self.get_options_dir(self.path))
        self.crop_type = st.selectbox("Select your Crop", crops, index = None, placeholder='Select')

        if self.crop_type: 
            self.path = os.path.join(self.path, self.crop_type.lower())
            self.path = self.get_filename()
        
        return self.path

    def __call__(self):
        self.format()
        path = self.get_path()

        if path and self.crop_type:
        # Making visualization of the village
            self.add_parcel_map(path)
        self.m.to_streamlit(layout = 'wide')
        
        # side bar
        claim = st.sidebar.radio("Select which data to see:", ["Prevented Sowing", "Yield Loss", "Localised Calamities", "Crop Loss"])



title_name = 'Claims Data'
path = r'data/claims'
# colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = 'Cause of L'
popup = ["Cause of L", 'Claims A_1']
aliases = ['Cause of Loss:', 'Claim Amount:']

claims_map(title_name, color_column, popup, aliases, path)()
