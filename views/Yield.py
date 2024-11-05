import streamlit as st
from main import base
import os

st.set_page_config(layout="wide")

class yield_map(base):
    def __init__(self, title_name, color_column, popup, aliases):
        super().__init__(title_name, color_column, popup, aliases)

    def get_path(self):
        # Making selectbox
        # c5 = st.columns(1)
        crops = []
        if self.year: crops.append("Soybean")
        self.crop_type = st.selectbox("Select your Crop", crops, index = None, placeholder='Select')

        path = None
        path = r"yield"

        if self.district == 'Mathura':
            path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
        elif self.district == 'Bhiwani':
            path = os.path.join(path, 'bhiwani')
            if self.year == '2024':
                path = os.path.join(path, '2024')
                if self.crop_type == 'Cotton':
                    path = os.path.join(path, 'cotton', '2024_cotton_yield_bhiwani_ajitpur.shp')
                elif self.crop_type == 'Pearl Millet':
                    path = os.path.join(path, 'pearl_millet', '2024_pearlmillet_yield_bhiwani_ajitpur.shp')
        else:
            path = os.path.join(path, 'vidisha')
            if self.year == '2022':
                path = os.path.join(path, '2022', 'soybean', "2022_ZONAL.shp")
            else:
                path = os.path.join(path, '2024', 'soybean', "2024_ZONALL.shp")

        return path

    def __call__(self):
        self.format()
        path = self.get_path()

        if path and self.crop_type:
        # Making visualization of the village
            self.add_parcel_map(path)
        self.m.to_streamlit(layout = 'wide')


title_name = 'Yield Map'
# colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = 'yie_cate'
popup = ['yie_cate', 'y(kg/ha)']
aliases = ['Yield Category:', 'Yield (Kg/Hec):']

yield_map(title_name, color_column, popup, aliases)()
