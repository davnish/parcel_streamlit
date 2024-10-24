import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
# import folium
import leafmap.foliumap as leafmap
# from branca.colormap import linear
# import branca.colormap as cm
# from branca.element import MacroElement, Template
import leafmap.colormaps as cm
import os
st.set_page_config(layout="wide")


st.title('Yield Map')
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

logo_path = r"C:\Users\AH-Nischal-Singh\Downloads\file-removebg-preview.png"
sidebar_path = r"C:\Users\AH-Nischal-Singh\Downloads\file-removebg-preview.png"


st.logo(sidebar_path, icon_image=logo_path, size = 'large')
st.sidebar.image(logo_path)

# This function is for read parcel amp
# @st.cache_resource
def read_parcel_map(gdf, _m, year, ):
    # gdf = gpd.read_file(path)
    # yield_cate = 
    yield_cate = 'yie_cate'

    gdf_idx = gdf[yield_cate]


    # colormap = cm.StepColormap(["red", "yellow", "blue"], vmin=0, vmax=len(gdf_idx.unique()), caption="Yield", )

    colormap = ["#FF0000", "#00FF00", "#0000FF"]

    legend_dict = {cate : color for cate, color in zip(sorted(gdf_idx.unique()), colormap)}


    color_dict = {key: colormap[idx] for idx, key in enumerate(sorted(gdf_idx.unique()))}
    # color_dict = {}
    color_dict = {key: color_dict[gdf_idx[key]] for key in gdf_idx.keys()}


    style_function=lambda feature: {
        "fillColor": color_dict[int(feature['id'])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    }

    gdf['Yield Category: '] = gdf.loc[:, 'yie_cate']
    gdf['Yield (Kg/Hec): '] = gdf.loc[:, 'y(kg/ha)']
    gdf = gdf.loc[:, ['Yield Category: ', 'Yield (Kg/Hec): ','geometry']]
    _m.add_gdf(gdf, layer_name = "Yield", zoom_on_click=True, style_function=style_function, )


    # _m.add_child(colormap)

    return _m, legend_dict



def get_map(path, year, raster_path = None):
    gdf = gpd.read_file(path)

    
    m = leafmap.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=14, draw_control=None)
    m.add_basemap("SATELLITE")
    # Raster Overlay
    
    m, legend_dict = read_parcel_map(gdf, m, year)

    m.add_legend(title="Yield Category", legend_dict=legend_dict, draggable=False)
    # m.add_raster(raster_path, colormap= 'terrain', layer_name=f"Raster {year}")
    m.to_streamlit(layout = 'wide')

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
            path = os.path.join(path,'2022', "2022_ZONAL.shp")
            # raster_path = r"D:\projects\parcel_streamlit\yield\vidisha\2022\2022.tif"
        else:
            path = os.path.join(path, '2024', "2024_ZONALL.shp")
            # raster_path = r"D:\projects\parcel_streamlit\yield\vidisha\2022\2024.tif"

    # Making visualization of the village





    get_map(path, year, raster_path)

    # Making Claims Graphs
