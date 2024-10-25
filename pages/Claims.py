import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
import leafmap.foliumap as leafmap

# import folium
# from branca.colormap import linear
# import branca.colormap as cm
import os

st.set_page_config(layout="wide")

logo_path = r"misc\logo\file-removebg-preview.png"
sidebar_path = r"misc\logo\file-removebg-preview.png"


st.logo(sidebar_path, icon_image=logo_path, )
st.sidebar.image(logo_path)

st.title('Claims Data')

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

# This function is for read parcel amp
# @st.cache_resource
def read_parcel_map(gdf, _m, year):
    # gdf = gpd.read_file(path)
    # 'Cause of L' = year + '_Crop'

    gdf_idx = gdf['Cause of L']

    if len(gdf_idx.unique()) == 4: 
        colormap = ["#0000FF",  "#000000", "#FFFF00", "#FF0000"]
    else:
        colormap = ["#0000FF", "#000000", "#FF0000"]

    legend_dict = {cate : color for cate, color in zip(sorted(gdf_idx.unique()), colormap)}

    color_dict = {key: colormap[idx] for idx, key in enumerate(sorted(gdf_idx.unique()))}
    color_dict = {key: color_dict[gdf_idx[key]] for key in gdf_idx.keys()}


    style_function=lambda feature: {
        "fillColor": color_dict[int(feature['id'])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    }
    
    gdf['Cause of Loss: '] = gdf.loc[:, "Cause of L"]
    gdf['Claim Amount: '] = gdf.loc[:, 'Claims A_1']
    gdf = gdf.loc[:, ['Cause of Loss: ', 'Claim Amount: ', 'geometry']]
    _m.add_gdf(gdf, layer_name = "Claim", zoom_on_click=True, style_function=style_function, highlight_function = lambda x: {'weight': 3, 'color': 'red'})

    return _m, legend_dict



def get_map(path, year, raster_path = None):
    gdf = gpd.read_file(path)

    
    m = leafmap.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=14, draw_control=None)
    m.add_basemap("SATELLITE")
    # Raster Overlay
    
    m, legend_dict = read_parcel_map(gdf, m, year)

    m.add_legend(title="Crop Type", legend_dict=legend_dict, draggable=False)
    m.to_streamlit(layout = 'wide')

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


    path = r"claims"
    if district == 'Mathura':
        path = os.path.join(path, 'mathura', '2022_soybean_claim_final.shp')
    elif district == 'Bhiwani':
        path = os.path.join(path, 'bhiwani', '2024_soybean_claim_final.shp')
    else:
        path = os.path.join(path, 'vidisha')

        if year == "2022":
            path = os.path.join(path, "2022", "2022_soybean_claim_final.shp")
        else: 
            path = os.path.join(path, "2024", "2024_soybean_claim_final.shp")

    # Making visualization of the village
    get_map(path, year)


    # Making Claims Graphs






