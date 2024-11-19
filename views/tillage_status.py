import streamlit as st
from util import base

if 'setting_page' not in st.session_state:
    st.set_page_config(layout="wide")
    st.session_state['setting_page'] = True

class sowing_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path, color_dict):
        super().__init__(title_name, color_column, popup, aliases, path, color_dict=color_dict)

    def get_path(self):
        self.path = self.get_filename(self.path)
        return self.path
    
    def add_parcel_map(self, path):
        self.color_column = self.year + '_Max'
        return super().add_parcel_map(path)

    def __call__(self):
        self.format()
        path = self.get_path()
        if path:
            # Making visualization of the village
            self.add_parcel_map(path)
        self.m.to_streamlit(layout = 'wide')



title_name = 'Tillage Status'
path = r'data/tillage'
color_column = None
popup = None
aliases = None
color_dict = {'01 June 2024 to 20 June 2024': 'red', '02-07-2022': 'green', '16-06-2022': 'blue', '18-07-2022': 'yellow',
              '05-06-2024': 'red',  '23-07-2024':'green', '21 June 2024 to 10 July 2024': 'pink',  '01 June 2024 to 15 June 2024': 'blue', '16 June 2024 to 30 June 2024': 'brown', '01 July 2024 to 15 July 2024': 'red'}
# legend_order = ['01 June 2024 to 20 June 2024', '21 June 2024 to 10 July 2024', '02-07-2022', '18-07-2022']
sowing_map(title_name, color_column, popup, aliases, path, color_dict = None)()
