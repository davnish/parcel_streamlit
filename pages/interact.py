import streamlit as st
import folium
from streamlit_folium import st_folium

# Streamlit App
st.title("Show Polygon Details on Click")

# Define the map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

# Sample GeoJSON data (polygons)
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Polygon 1", "info": "Details about Polygon 1"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-122.42, 37.78],
                    [-122.41, 37.78],
                    [-122.41, 37.77],
                    [-122.42, 37.77],
                    [-122.42, 37.78]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Polygon 2", "info": "Details about Polygon 2"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-122.43, 37.77],
                    [-122.42, 37.77],
                    [-122.42, 37.76],
                    [-122.43, 37.76],
                    [-122.43, 37.77]
                ]]
            }
        }
    ]
}

# Add GeoJSON layer to the map
folium.GeoJson(
    geojson_data,
    name="Polygons",
    style_function=lambda feature: {
        'fillColor': 'blue',
        'color': 'blue',
        'weight': 2,
        'fillOpacity': 0.5
    },
    highlight_function=lambda x: {'weight': 3, 'color': 'red'},
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Name:"]),
    popup=folium.GeoJsonPopup(fields=["name", "info"], aliases=["Name", "Info"])
).add_to(m)

# Render the map in Streamlit
st_data = st_folium(m, width=725)

# Show additional details when a polygon is clicked
if st_data and st_data["last_clicked"]:
    feature = st_data["last_clicked"]
    st.write(f"Clicked Polygon: {feature['properties']['name']}")
    st.write(f"Details: {feature['properties']['info']}")
