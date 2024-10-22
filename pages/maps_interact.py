import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium

# Sample file paths - Replace with actual paths
state_file = r'D:\projects\parcel_streamlit\admin_bounds\STATE_BOUNDARY.shp'
district_file = r'admin_bounds/DISTRICT_BOUNDARY.shp'
# village_file = 'path_to_village_geojson.geojson'

# Load data with GeoPandas
@st.cache_data
def read_shps():
    states = gpd.read_file(state_file)
    districts = gpd.read_file(district_file)
    return states, districts

states, districts = read_shps()
# villages = gpd.read_file(village_file)

# Create a sidebar dropdown for state selection
selected_state = st.sidebar.selectbox("Select a State", states['STATE'].unique())

# Filter districts based on selected state
filtered_districts = districts[districts['STATE'] == selected_state]

# Create a map using folium
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add state boundaries
for _, state in states.iterrows():
    if state['STATE'] == selected_state:
        folium.GeoJson(state['geometry'], name=state['STATE']).add_to(m)

# Add districts to the map with click functionality
for _, district in filtered_districts.iterrows():
    folium.GeoJson(district['geometry'],
                   name=district['District'],
                   popup=district['District'],
                   tooltip="Click to zoom",
                   zoom_on_click=True).add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)



# # If a district is clicked, show villages (nested interaction)
# selected_district = st.selectbox("Select a District", filtered_districts['district_name'].unique())

# if selected_district:
#     # Filter villages based on selected district
#     filtered_villages = villages[villages['district_name'] == selected_district]

#     # Create a new map zoomed into the selected district
#     m_villages = folium.Map(location=[filtered_villages['geometry'].centroid.y.mean(),
#                                       filtered_villages['geometry'].centroid.x.mean()],
#                             zoom_start=10)
    
#     # Add villages to the map
#     for _, village in filtered_villages.iterrows():
#         folium.GeoJson(village['geometry'],
#                        name=village['village_name'],
#                        popup=village['village_name'],
#                        tooltip="Click to view files").add_to(m_villages)

#     st_folium(m_villages, width=700, height=500)

#     # Village click logic to show vector files (e.g., shapefiles or raster files)
#     selected_village = st.selectbox("Select a Village", filtered_villages['village_name'].unique())

#     if selected_village:
#         # Logic to show vector files for the selected village
#         st.write(f"Showing vector files for village: {selected_village}")
#         # You can add download buttons or display shapefiles here.
