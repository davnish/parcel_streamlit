import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from branca.colormap import linear

st.title('AgronomIQ')

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

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

    path = 'gdf.shp'
    # st_data = st_folium(path width=700, )

    # Making visualization of the village

    gdf = gpd.read_file(path)
    print(gdf['KHASRA'])

    colormap = linear.Paired_10.scale(0, 1587)
    # gdf['sr'] = np.arange(0, 980)
    # gdf = gdf.set_index('sr')
    gdf_idx = gdf['KHASRA']
    color_dict = {key: colormap(gdf_idx[key]) for key in gdf_idx.keys()}

    # Showing ESRI Satellite Imagery
    tile = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
        )
    
    style_function=lambda feature: {
        "fillColor": color_dict[int(feature["id"])],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.3,
    }
    
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=16, tiles=tile)
    folium.GeoJson(gdf, zoom_on_click=True, highlight_function=lambda x: {'weight': 3, 'color': 'red'},
                tooltip=folium.GeoJsonTooltip(fields=["KHASRA"], aliases=["KHASRA"]),
                    popup=folium.GeoJsonPopup(fields=["TAHSIL", 'area_hecta'], aliases=["TEHSIL", 'area_hecta']),
                    style_function=style_function
                    ).add_to(m)

    folium.LayerControl().add_to(m)
    st_data = st_folium(m, width=700, )





