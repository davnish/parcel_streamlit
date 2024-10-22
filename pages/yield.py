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

custom_ticks = {0: "Low", 1: "Moderate", 2: "High"}


def custom_colormap_labels(colormap, custom_labels):
    html = colormap._repr_html_()

    for tick, label in custom_labels.items():
        html = html.replace(f">{tick}<", f">{label}<")

    return html

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

# This function is for reading point data
def read_point_data(path, m):
    gdf_point = gpd.read_file(path)

    # Reading Point Data
    folium.GeoJson(
    gdf_point,
    name="Info",
    marker=folium.Marker(icon=folium.DivIcon()),
    tooltip=folium.GeoJsonTooltip(fields=["Yield_str"]),
    popup=folium.GeoJsonPopup(fields=["Yield_cate", "Yield_str", "mean_q/ha"]),
    style_function=style_function_point,
    zoom_on_click=True,
    ).add_to(m)

# This function is for read parcel amp
# @st.cache_resource
def read_parcel_map(path, _m, year, ):
    gdf = gpd.read_file(path)
    # yield_cate = 
    yield_cate = 'yie_cate'

    gdf_idx = gdf[yield_cate]
    # gdf.set_index('khasra_uni')

    # colormap = cm.LinearColormap(["blue", "yellow", "red"], vmin=3, vmax=len(gdf_idx.unique()), caption = "Yield Loss")
    colormap = cm.StepColormap(["red", "yellow", "blue"], vmin=0, vmax=len(gdf_idx.unique()), caption="Yield")

    # html = colormap._repr_html_()
    # custom_legend = html.replace("0.0", "Low").replace("1.0", "Medium").replace("3.0", "High")


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
            tooltip=folium.GeoJsonTooltip(fields=[yield_cate]),
                popup=folium.GeoJsonPopup(fields=[yield_cate, "y(kg/h)"], aliases=["Yield Category: ", "Yield (Kg/h)"]),
                style_function=style_function
                ).add_to(_m)
    
    html = custom_colormap_labels(colormap, custom_ticks)
    _m.get_root().html.add_child(folium.Element(html))
    _m.save('custom_colormap_with_labels.html')

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
    
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=14, tiles=tile)

    # For Full Screen
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
with c4: year = st.selectbox("Select your Year", ["2022", "2023", "2024"])
with c5: crop_type = st.selectbox("Select your Crop", ["Soyabean"])

search = st.button('Search')

if search:
    st.session_state['button_clicked'] = True

if st.session_state['button_clicked']:


    path = r"yield"
    if district == 'Mathura':
        path = os.path.join(path, 'mathura', 'Combined_mathura_nagladhanua.shp')
    elif district == 'Bhiwani':
        path = os.path.join(path, 'bhiwani', 'Final_Bhiwani_village_Bhiwani.shp')
    else:
        path = os.path.join(path, 'vidisha', 'Vidisha_Yield_22_Parcels.shp')
    # Making visualization of the village
    get_map(path, year)


    # Making Claims Graphs
