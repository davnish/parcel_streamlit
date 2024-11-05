import streamlit as st
import os
from main import base
import os

class crop_map(base):
    def __init__(self, title_name, color_column, popup, aliases, colormap=None):
        super().__init__(title_name, color_column, popup, aliases, colormap)

    def get_path(self):
        # Making selectbox
        admin_bounds = 'admin_bounds'

        self.set_map()
        c1, c2, c3, c4, c5 = st.columns(5)

        with c1: state = st.selectbox("Select your State:", ['Madhya Pradesh', 'Uttar Pradesh', 'Haryana'], index = None, placeholder='Select')
        
        district = []
        village = []
        block = []
        year = []

        state_bounds = os.path.join(admin_bounds , 'state_boundary')
        if state == 'Madhya Pradesh':
            district.append('Vidisha')
            block.append('Kurwai')
            village.append('Bhaunrasa')
            year.extend(['2022', '2024'])

            self.add_map(os.path.join(state_bounds, "mp", "mp_state_boundary.shp"), state)

        elif state == 'Uttar Pradesh':
            district.append('Mathura')
            block.append('Mahavan')
            village.append('Nagla Dhanua')
            year.extend(['2022', '2024'])

            self.add_map(os.path.join(state_bounds, "up", "UP_state_boundary.shp"), state)

        elif state == 'Haryana':
            district.append('Bhiwani')
            block.append('Bhiwani')
            village.append('Ajitpur')
            year.extend(['2022', '2024'])

            self.add_map(os.path.join(state_bounds, "haryana", "haryana_state_boundary.shp"), state)

        with c2: district = st.selectbox("Select your District:", district,  index = None, placeholder='Select')
        
        district_bounds = os.path.join(admin_bounds, 'district_boundary')
        if district == 'Vidisha':
            self.add_map(os.path.join(district_bounds, 'vidisha', 'vidisha_district.shp'), district)
        if district == 'Bhiwani':
            self.add_map(os.path.join(district_bounds, 'bhiwani', 'BHIWANI_DISTRICT.shp'), district)
        if district == 'Mathura':
            self.add_map(os.path.join(district_bounds, 'mathura', 'mathura_district.shp'), district)
        
        with c3: block = st.selectbox("Select your Tehsil:", block ,  index = None, placeholder='Select')
        
        block_bounds = os.path.join(admin_bounds, 'subdistrict_boundary')
        if block == 'Kurwai':
            self.add_map(os.path.join(block_bounds, 'kurwai/VIDISHA_SUDISTRICT.shp'), block)
        if block == 'Bhiwani':
            self.add_map(os.path.join(block_bounds,'bhiwani/Bhiwani_subdist.shp'), block)
        if block == 'Mahavan':
            self.add_map(os.path.join(block_bounds, 'mahavan/mathura_subdistrict.shp'), block)
        
        with c4: village = st.selectbox("Select your Village:", village,  index = None, placeholder='Select')
        
        village_bounds = os.path.join(admin_bounds, 'village_boundary')
        if village == 'Bhaunrasa':
            self.add_map(os.path.join(village_bounds, 'Bhaunrasa/vidisha_village_boundary.shp'), village)
        if village == 'Ajitpur':
            self.add_map(os.path.join(village_bounds, 'Ajitpur/BHIWANI_VILLAGE_AJITPUR.shp'), village)
        if village == 'Nagla Dhanua':
            self.add_map(os.path.join(village_bounds, 'Nagla_Dhanua/mathura_village_boundary.shp'), village)
        
        with c5: self.year = st.selectbox("Select your Year", year,  index = None, placeholder='Select')
        
        path = None
        path = r"crop_type"

        if district == 'Mathura':
            path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
        elif district == 'Bhiwani':
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
        path = self.get_path()
        print(path)
        if path and self.year:
            # Making visualization of the village
            self.add_parcel_map(path)

        self.m.to_streamlit(layout = 'wide')
        


title_name = 'Crop Map'
colormap = None
# colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = None
popup = ['khasranum_']
aliases = ['Khasra No:']

crop_map(title_name, color_column, popup, aliases, colormap=colormap)()







