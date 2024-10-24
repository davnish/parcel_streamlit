import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from branca.colormap import linear
import branca.colormap as cm

st.title('AgronomIQ')

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

def style_function_point(feature):
    props = feature.get('properties')
    markup = f"""
        <a href="{props.get('url')}">
            <div style="font-size: 0.8em;">
            <div style="width: 10px;
                        height: 10px;
                        border: 1px solid black;
                        border-radius: 5px;
                        background-color: orange;">
            </div>
            {props.get('name')}
        </div>
        </a>
    """
    return {"html": markup}


# This function is for read parcel amp
# @st.cache_resource
def read_parcel_map(path, _m):
    gdf = gpd.read_file(path)

    gdf_idx = gdf['khasra_uni']
    # gdf.set_index('khasra_uni')

    colormap = cm.LinearColormap(["blue", "green", "yellow", "red"], vmin=gdf_idx.min(), vmax=gdf_idx.max())

    color_dict = {key: colormap(key) for key in gdf_idx.unique()}
    color_dict = {key: color_dict[gdf_idx[key]] for key in gdf_idx.keys()}
    # print(np.unique([val for val in color_dict.values()]))

    style_function=lambda feature: {
        "fillColor": color_dict[int(feature['id'])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    }
    folium.GeoJson(gdf, zoom_on_click=True, highlight_function=lambda x: {'weight': 3, 'color': 'red'}, name = "parcel_map",
            tooltip=folium.GeoJsonTooltip(fields=["KHASRA"], aliases=["KHASRA"]),
                popup=folium.GeoJsonPopup(fields=["TEHSIL", 'Area (in h'], aliases=["Tehsil", 'area_hecta']),
                style_function=style_function
                ).add_to(_m)
    
    return _m

# This function is for reading point data
def read_point_data(path, m):
    gdf_point = gpd.read_file(path)

    # Reading Point Data
    folium.GeoJson(
    gdf_point,
    name="Info",
    marker=folium.Marker(icon=folium.DivIcon()),
    tooltip=folium.GeoJsonTooltip(fields=["KHASRA"]),
    popup=folium.GeoJsonPopup(fields=["KHASRA"]),
    style_function=style_function_point,
    zoom_on_click=True,
    ).add_to(m)


def get_map(path):
    gdf = gpd.read_file(path)

    # Showing ESRI Satellite Imagery
    tile = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
        )
    
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=16, tiles=tile)
    m = read_parcel_map(path, m)

    folium.LayerControl().add_to(m)
    st_data = st_folium(m, width=700, )

# Making selectbox
c1, c2, c3 = st.columns(3)

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

search = st.button('Search')

if search:
    st.session_state['button_clicked'] = True

if st.session_state['button_clicked']:

    path = r"D:\projects\parcel_streamlit\vidisha\Combined_crop_map.shp"

    # Making visualization of the village
    get_map(path)
    
    # Making Claims Graphs






