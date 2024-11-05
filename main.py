import streamlit as st
# from streamlit_folium import st_folium
# import pandas as pd
# import numpy as np
import matplotlib.colors as mcolors
import geopandas as gpd
import leafmap.foliumap as leafmap
import leafmap.colormaps as cm
import os


class base:
    def __init__(self, title_name, color_column, popup, aliases, legend_order = None):
        
        self.color_dict = {'Low': 'red', 'High': 'green', 'Healthy': 'green', 'Moderate': 'blue', 
              'Blackgram': 'blue', 'Paddy': 'yellow', 'Soybean': 'red', 'No Claim': 'blue', 
              'No Data': 'black', 'Prevented Sowing': 'yellow', 'Yield Loss': 'red', 
              'Cotton': 'white', 'Pearl Millet': 'brown', 'No crop': 'black' }
        
        self.title_name = title_name
        self.color_column = color_column
        self.popup = popup
        self.aliases = aliases
        self.legend_order = legend_order
        # if colormap is not None: self.colormap = colormap
        # else: self.colormap = cm.get_palette("Paired")
        # print(self.colormap) 
        st.set_page_config(page_title=f"{title_name}", page_icon="🌏",layout="wide")

        logo_path = os.path.join("misc", "logo", "file-removebg-preview.png")
        sidebar_path = os.path.join("misc", "logo", "file-removebg-preview.png")

        st.logo(sidebar_path, icon_image=logo_path)
        st.sidebar.image(logo_path)

        st.title(f'{title_name}')

        if 'selected' not in st.session_state:
            st.session_state['selected'] = False

    # @st.cache_data
    def get_data(self, path):
        print(path)
        gdf = gpd.read_file(path)
        return gdf

    def add_map(self, path, layer_name, color=None):
        if color is None:
            color = 'blue'

        line_style = {
            'color': color,      # Line color
            'weight': 4,          # Line thickness
            'dashArray': '7, 7',
            'fillOpacity': 0   # Creates a dashed effect: "5px line, 5px space"
        }

        gdf = gpd.read_file(path)
        self.m.add_gdf(gdf, style = line_style, layer_name = layer_name)
        self.m.set_center(lat=gdf.geometry.centroid.y.mean(), lon=gdf.geometry.centroid.x.mean(), zoom=10)
        
    # This function is for read parcel amp
    def add_parcel_map(self, path):
        self.gdf = self.get_data(path)
        gdf_idx = self.gdf[self.color_column]

        if self.legend_order is None:
            legend_dict = {cate : mcolors.CSS4_COLORS[self.color_dict[cate]] for cate in sorted(gdf_idx.unique())}
        else:
            legend_dict = {cate : mcolors.CSS4_COLORS[self.color_dict[cate]] for cate in self.legend_order}
            
        
        color_dict = {key: legend_dict[gdf_idx[key]] for key in gdf_idx.keys()}

        style_function=lambda feature: {
            "fillColor": color_dict[int(feature['id'])],
            "color": "black",
            "weight": 1,
            "fillOpacity": 1,
        }
        
        for name, col in zip(self.aliases, self.popup):
            self.gdf.rename(columns = {col:name}, inplace = True)

        self.m.add_gdf(self.gdf.loc[:, [*self.aliases, 'geometry']], 
                       layer_name = f"{self.title_name}", zoom_on_click=True, 
                       style_function=style_function, 
                       highlight_function = lambda x: {'weight': 3, 'color': 'red'})
        
        
        self.m.add_legend(title=f"{self.title_name}", legend_dict=legend_dict, draggable=False)
        self.m.set_center(lat=self.gdf.geometry.centroid.y.mean(),lon=self.gdf.geometry.centroid.x.mean(), zoom = 14 )

    
    def set_map(self):
        # gdf = self.get_data(path)
        self.m = leafmap.Map(location = [22.176,78.410], zoom_start=5, draw_control=None)
        self.m.add_basemap("SATELLITE")
    
    def format(self):
        admin_bounds = 'admin_bounds'

        self.set_map()
        c1, c2, c3, c4, c5 = st.columns(5)

        with c1: state = st.selectbox("Select your State:", ['Madhya Pradesh', 'Uttar Pradesh', 'Haryana'], index = None, placeholder='Select')
        
        district = []
        village = []
        block = []
        year = []

        state_bound_color = '#661100'
        dist_bound_color = '#6699CC'
        block_bound_color = '#71035e'
        village_bound_color = '#000000'

        state_bounds = os.path.join(admin_bounds , 'state_boundary')
        if state == 'Madhya Pradesh':
            district.append('Vidisha')
            block.append('Kurwai')
            village.append('Bhaunrasa')
            year.extend(['2022', '2023', '2024'])
            self.add_map(os.path.join(state_bounds, "mp", "mp_state_boundary.shp"), state, state_bound_color)

        elif state == 'Uttar Pradesh':
            district.append('Mathura')
            block.append('Mahavan')
            village.append('Nagla Dhanua')
            year.extend(['2022', '2023','2024'])

            self.add_map(os.path.join(state_bounds, "up", "UP_state_boundary.shp"), state, state_bound_color)

        elif state == 'Haryana':
            district.append('Bhiwani')
            block.append('Bhiwani')
            village.append('Ajitpur')
            year.extend(['2022', '2023','2024'])

            self.add_map(os.path.join(state_bounds, "haryana", "haryana_state_boundary.shp"), state, state_bound_color)

        with c2: self.district = st.selectbox("Select your District:", district,  index = None, placeholder='Select')
        
        district_bounds = os.path.join(admin_bounds, 'district_boundary')

        if self.district == 'Vidisha':
            self.add_map(os.path.join(district_bounds, 'vidisha', 'vidisha_district.shp'), self.district, dist_bound_color)
        elif self.district == 'Bhiwani':
            self.add_map(os.path.join(district_bounds, 'bhiwani', 'BHIWANI_DISTRICT.shp'), self.district, dist_bound_color)
        elif self.district == 'Mathura':
            self.add_map(os.path.join(district_bounds, 'mathura', 'mathura_district.shp'), self.district, dist_bound_color)
        
        with c3: block = st.selectbox("Select your Tehsil:", block ,  index = None, placeholder='Select')
        
        block_bounds = os.path.join(admin_bounds, 'subdistrict_boundary')
        if block == 'Kurwai':
            self.add_map(os.path.join(block_bounds, 'kurwai/VIDISHA_SUDISTRICT.shp'), block, block_bound_color)
        elif block == 'Bhiwani':
            self.add_map(os.path.join(block_bounds,'bhiwani/Bhiwani_subdist.shp'), block, block_bound_color)
        elif block == 'Mahavan':
            self.add_map(os.path.join(block_bounds, 'mahavan/mathura_subdistrict.shp'), block, block_bound_color)
        
        with c4: village = st.selectbox("Select your Village:", village,  index = None, placeholder='Select')
        
        village_bounds = os.path.join(admin_bounds, 'village_boundary')
        if village == 'Bhaunrasa':
            self.add_map(os.path.join(village_bounds, 'Bhaunrasa/vidisha_village_boundary.shp'), village, village_bound_color)
        elif village == 'Ajitpur':
            self.add_map(os.path.join(village_bounds, 'Ajitpur/BHIWANI_VILLAGE_AJITPUR.shp'), village, village_bound_color)
        elif village == 'Nagla Dhanua':
            self.add_map(os.path.join(village_bounds, 'Nagla_Dhanua/mathura_village_boundary.shp'), village, village_bound_color)
        
        with c5: self.year = st.selectbox("Select your Year", year,  index = None, placeholder='Select')

# --- Page Setup ---

crop_map = st.Page(
    page = "views/Crop_Map.py",
    title = "Crop Map",
    icon = "🗺️",
    default = True
)

yield_map = st.Page(
    page = "views/Yield.py",
    title = "Yield Map",
    icon = "🌾",
)

sowing_status = st.Page(
    page = "views/sowing_status.py",
    title = "Sowing Status",
    icon = "👨🏽‍🌾",
)

claims = st.Page(
    page = "views/Claims.py",
    title = "Claims",
    icon = "📊",
)

weather_data = st.Page(
    page = "views/weather_data.py",
    title = "Weather Data",
    icon = "🌤️",
)

chm = st.Page(
    page = "views/CHM.py",
    title = "Crop Health Monitoring",
    icon = "🌱"
)
# -- Setting Navigation --

pg = st.navigation(pages = [sowing_status, crop_map, chm, yield_map, claims, weather_data])

# -- Run Nav --

pg.run()