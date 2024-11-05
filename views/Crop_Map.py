import streamlit as st
import os
from main import base
import os
st.set_page_config(layout="wide")

class crop_map(base):
    def __init__(self, title_name, color_column, popup, aliases):
        super().__init__(title_name, color_column, popup, aliases)

    def get_path(self):
        # Making selectbox
                
        path = None
        path = r"crop_type"

        if self.district == 'Mathura':
            path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
        elif self.district == 'Bhiwani':
            path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
        else:
            path = os.path.join(path, 'vidisha', 'vidisha_croptype_final.shp')
        return path
    
    
    def add_parcel_map(self, path):
        self.color_column = self.year + '_Crop'
        self.popup.append(f'{self.year}_Crop')
        self.aliases.append(f'Crop Type: ')

        return super().add_parcel_map(path)
                
    def __call__(self):
        self.format()
        path = self.get_path()
        print(path)
        if path and self.year:
            # Making visualization of the village
            self.add_parcel_map(path)

        self.m.to_streamlit(layout = 'wide')
        


title_name = 'Crop Map'
# colormap = None/
# colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = None
popup = ['khasranum_']
aliases = ['Khasra No:']

crop_map(title_name, color_column, popup, aliases)()







