import streamlit as st
from main import base
st.set_page_config(layout="wide")

class crop_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path):
        super().__init__(title_name, color_column, popup, aliases, path)

    def get_path(self):
        if self.year: self.path = self.get_filename()
        
        return self.path
    
    
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
path = r'data/crop_map'
color_column = None
popup = ['KHASRA', 'area_hecta']
aliases = ['Khasra No:', 'Area (hectare)']

crop_map(title_name, color_column, popup, aliases, path)()







