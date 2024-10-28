import streamlit as st
# from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
import leafmap.foliumap as leafmap
import leafmap.colormaps as cm
import os


class base:
    def __init__(self, title_name, color_column, popup, aliases, colormap = None):
        self.title_name = title_name
        self.color_column = color_column
        self.popup = popup
        self.aliases = aliases
        if colormap is not None: self.colormap = colormap
        else: self.colormap = cm.get_palette("Set1")

        st.set_page_config(page_title=f"{title_name}", page_icon="🦜",layout="wide")

        logo_path = os.path.join("misc", "logo", "file-removebg-preview.png")
        sidebar_path = os.path.join("misc", "logo", "file-removebg-preview.png")

        st.logo(sidebar_path, icon_image=logo_path)
        st.sidebar.image(logo_path)

        st.title(f'{title_name}')

        if 'button_clicked' not in st.session_state:
            st.session_state['button_clicked'] = False

    # @st.cache_data
    def get_data(self, path):
        print(path)
        gdf = gpd.read_file(path)
        return gdf

    def get_map(self, path):
        self.gdf = self.get_data(path)
        self.m = leafmap.Map(location=[self.gdf.geometry.centroid.y.mean(), self.gdf.geometry.centroid.x.mean()], zoom_start=14, draw_control=None)
        self.m.add_basemap("SATELLITE")

        legend_dict = self.add_parcel_map()
        self.m.add_legend(title=f"{self.title_name}", legend_dict=legend_dict, draggable=False)
        self.m.to_streamlit(layout = 'wide')
        
    # This function is for read parcel amp
    def add_parcel_map(self):

        gdf_idx = self.gdf[self.color_column]



        legend_dict = {cate : self.colormap[i] for i, cate in enumerate(sorted(gdf_idx.unique()))}
        color_dict = {key: legend_dict[gdf_idx[key]] for key in gdf_idx.keys()}

        style_function=lambda feature: {
            "fillColor": color_dict[int(feature['id'])],
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.5,
        }
        
        for name, col in zip(self.aliases, self.popup):
            self.gdf.rename(columns = {col:name}, inplace = True)

        self.m.add_gdf(self.gdf.loc[:, [*self.aliases, 'geometry']], 
                       layer_name = f"{self.title_name}", zoom_on_click=True, 
                       style_function=style_function, 
                       highlight_function = lambda x: {'weight': 3, 'color': 'red'})

        return legend_dict