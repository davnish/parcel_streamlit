import streamlit as st
from util import base
import os

if 'setting_page' not in st.session_state:
    st.set_page_config(layout="wide")
    st.session_state['setting_page'] = True

class yield_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path, legend_order):
        super().__init__(title_name, color_column, popup, aliases, path, legend_order=legend_order)

    def get_path(self):
        crops = []
        if self.year: crops.extend(self.get_options_dir())
        self.crop_type = st.selectbox("Select your Crop", crops, index = None, placeholder='Select')

        if self.crop_type: 
            self.path = os.path.join(self.path, self.crop_type.lower())
            self.path = self.get_filename(self.path)
        
        # return self.path

    def __call__(self):
        self.format()
        self.get_path()

        if self.crop_type:
        # Making visualization of the village
            self.add_parcel_map(self.path)
            
        self.m.to_streamlit(layout = 'wide')


title_name = 'Yield Prediction'
# colormap = ["#FF0000", "#00FF00", "#0000FF"]
path = r'data/yield'
color_column = 'yie_cate'
legend_order = ['High', 'Moderate', 'Low']
popup = ['yie_cate', 'y(kg/ha)']
aliases = ['Yield Category:', 'Yield (Kg/Hec):']

yield_map(title_name, color_column, popup, aliases, path, legend_order=legend_order)()