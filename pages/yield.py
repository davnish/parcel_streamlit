import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from branca.colormap import linear
import branca.colormap as cm
from branca.element import MacroElement, Template
import os

st.title('AgronomIQ')
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

logo_path = r"C:\Users\AH-Nischal-Singh\Downloads\image-removebg-preview (1).png"
sidebar_path = r"C:\Users\AH-Nischal-Singh\Downloads\image-removebg-preview (2).png"
st.logo(sidebar_path, icon_image=logo_path, size='large')

# This function is for read parcel amp
# @st.cache_resource
def read_parcel_map(path, _m, year, ):
    gdf = gpd.read_file(path)
    # yield_cate = 
    yield_cate = 'yie_cate'

    gdf_idx = gdf[yield_cate]

    colormap = cm.StepColormap(["red", "yellow", "blue"], vmin=0, vmax=len(gdf_idx.unique()), caption="Yield", )

    color_dict = {key: colormap(idx) for idx, key in enumerate(sorted(gdf_idx.unique()))}
    color_dict = {key: color_dict[gdf_idx[key]] for key in gdf_idx.keys()}


    style_function=lambda feature: {
        "fillColor": color_dict[int(feature['id'])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    }


    folium.GeoJson(gdf, zoom_on_click=True, highlight_function=lambda x: {'weight': 3, 'color': 'red'}, name = "parcel_map",
            tooltip=folium.GeoJsonTooltip(fields=[yield_cate], aliases=["Yield Category: "]),
                popup=folium.GeoJsonPopup(fields=[yield_cate, "y(kg/ha)"], aliases=["Yield Category: ", "Yield (Kg/h): "]),
                style_function=style_function
                ).add_to(_m)

    _m.add_child(colormap)

    return _m



def get_map(path, year, raster_path = None):
    gdf = gpd.read_file(path)

    # Showing ESRI Satellite Imagery
    tile = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
        )
    
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=14, tiles=tile)
    
    # Raster Overlay
    if raster_path is not None:
        folium.raster_layers.ImageOverlay(image=raster_path, bounds=[78.0020684509999995,24.1270070809999986,78.0366781390000028,24.1595161810000008]).add_to(m)
    

    # For Full Screen
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(m)
    m = read_parcel_map(path, m, year)
    # m.add_legend(title="hello", legend_dict = legend_dict)
    folium.LayerControl().add_to(m)
    st_data = st_folium(m, width=700, )

# Making selectbox
c1, c2, c3, c4, c5 = st.columns(5)

with c1: state = st.selectbox("Select your State:", ['Madhya Pradesh'])


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
with c5: crop_type = st.selectbox("Select your Crop", ["Soybean"])

search = st.button('Search')

if search:
    st.session_state['button_clicked'] = True

if st.session_state['button_clicked']:

    raster_path = None
    path = r"yield"
    if district == 'Mathura':
        path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
    elif district == 'Bhiwani':
        path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
    else:
        path = os.path.join(path, 'vidisha')
        if year == '2022':
            path = os.path.join(path,'2022', '22_Vidisha_Soybean_Yield_Zonal_Parcels.shp')
            # raster_path = r"D:\projects\parcel_streamlit\yield\vidisha\2022\Vidisha_Bhaumrasa_Yield_Map.tif"
        else:
            path = os.path.join(path, '2023', 'Bhaumrasa_24_final_manipulated_yield.shp')
            # raster_path = r'D:\projects\parcel_streamlit\yield\vidisha\2022\Vidisha_Bhaumrasa_Yield_Map.tif'

    # Making visualization of the village





    get_map(path, year, raster_path)

    # Making Claims Graphs
