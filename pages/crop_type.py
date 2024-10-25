import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd

import leafmap.foliumap as leafmap
import os


def read_parcel_map(gdf, _m, year):
    # gdf = gpd.read_file(path)
    crop_year = year + '_Crop'

    gdf_idx = gdf[crop_year]
    # gdf.set_index('khasra_uni')

    # colormap = cm.LinearColormap(["blue", "yellow", "red"], vmin=0, vmax=len(gdf_idx.unique()))
    if len(gdf_idx.unique()) == 4: 
        colormap = ["#0000FF",  "#000000", "#FFFF00", "#FF0000"]
    else:
        colormap = ["#0000FF", "#FFFF00", "#FF0000"]

    legend_dict = {cate : color for cate, color in zip(sorted(gdf_idx.unique()), colormap)}

    color_dict = {key: colormap[idx] for idx, key in enumerate(sorted(gdf_idx.unique()))}
    color_dict = {key: color_dict[gdf_idx[key]] for key in gdf_idx.keys()}


    style_function=lambda feature: {
        "fillColor": color_dict[int(feature['id'])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    }

    gdf['Crop Type: '] = gdf.loc[:, crop_year]
    gdf = gdf.loc[:, ['Crop Type: ','geometry']]
    _m.add_gdf(gdf, layer_name = "Crop Type", zoom_on_click=True, style_function=style_function, highlight_function = lambda x: {'weight': 3, 'color': 'red'})



    return _m, legend_dict


def get_map(path, year, raster_path = None):
    gdf = gpd.read_file(path)

    
    m = leafmap.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=14, draw_control=None)
    m.add_basemap("SATELLITE")
    # Raster Overlay
    
    m, legend_dict = read_parcel_map(gdf, m, year)

    m.add_legend(title="Crop Type", legend_dict=legend_dict, draggable=False)
    m.to_streamlit(layout = 'wide')
    if st.checkbox('Show Table: '):
        st.table(gdf.loc[:, ['khasranum_', '2022_Crop', '2024_Crop']])

# Making selectbox
c1, c2, c3, c4 = st.columns(4)

with c1: state = st.selectbox("Select your State:", ['Madhya Pradesh', 'Uttar Pradesh', 'Haryana'])


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
with c3: village = st.selectbox("Select your Village:", village)
with c4: year = st.selectbox("Select your Year", ["2022", "2024"])

search = st.button('Search')

if search:
    st.session_state['button_clicked'] = True

if st.session_state['button_clicked']:


    path = r"crop_type"
    if district == 'Mathura':
        path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
    elif district == 'Bhiwani':
        path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
    else:
        path = os.path.join(path, 'vidisha', 'vidisha_croptype_final.shp')
        
    # Making visualization of the village
    get_map(path, year)


    # Making Claims Graphs






