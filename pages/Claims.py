import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from branca.colormap import linear
import branca.colormap as cm
import os

st.title('AgronomIQ')

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

# This function is for read parcel amp
# @st.cache_resource
def read_parcel_map(path, _m, year):
    gdf = gpd.read_file(path)
    # 'Cause of L' = year + '_Crop'

    gdf_idx = gdf['Cause of L']

    if len(gdf_idx.unique()) == 4: 
        colors = ["blue", "green", "yellow", "red"]
    else:
        colors = ["yellow", "black", "red"]

    colormap = cm.StepColormap(colors, vmin=0, vmax=len(gdf_idx.unique()), caption="Crop Type")
    _m.add_child(colormap)

    color_dict = {key: colormap(idx) for idx, key in enumerate(sorted(gdf_idx.unique()))}
    color_dict = {key: color_dict[gdf_idx[key]] for key in gdf_idx.keys()}
    # print(np.unique([val for val in color_dict.values()]))

    style_function=lambda feature: {
        "fillColor": color_dict[int(feature['id'])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    }
    folium.GeoJson(gdf, zoom_on_click=True, highlight_function=lambda x: {'weight': 3, 'color': 'red'}, name = "parcel_map",
            tooltip=folium.GeoJsonTooltip(fields=['Cause of L'], aliases=["Cause of Loss: "]),
                popup=folium.GeoJsonPopup(fields=['Cause of L', "Claims A_1"], aliases=["Cause of Loss: ", "Claims Amount: "]),
                style_function=style_function
                ).add_to(_m)
    
    return _m



def get_map(path, year):
    gdf = gpd.read_file(path)

    # Showing ESRI Satellite Imagery
    tile = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
        )
    
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=15, tiles=tile)
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(m)
    m = read_parcel_map(path, m, year)

    folium.LayerControl().add_to(m)
    st_data = st_folium(m, width=700, )

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
        path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
    elif district == 'Bhiwani':
        path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
    else:
        path = os.path.join(path, 'vidisha')

        if year == "2022":
            path = os.path.join(path, "2022", "Claims_2022.shp")
        else: 
            path = os.path.join(path, "2024", "Claims_2024.shp")

    # Making visualization of the village
    get_map(path, year)


    # Making Claims Graphs






