import folium
from branca.element import Template, MacroElement
from streamlit_folium import st_folium

# Create a Folium map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Define a custom legend with HTML and CSS
legend_html = '''
     <div style="position: fixed; 
     bottom: 800px; left: 1000px; width: 150px; height: 100px; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; padding: 10px;">
     <b>Legend</b><br>
     <i style="background: red; width: 10px; height: 10px; float: left; margin-right: 8px;"></i>Low<br>
     <i style="background: green; width: 10px; height: 10px; float: left; margin-right: 8px;"></i>Moderate<br>
     <i style="background: blue; width: 10px; height: 10px; float: left; margin-right: 8px;"></i>High<br>
     </div>
     '''

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))
folium.plugins.Fullscreen(
position="topright",
title="Expand me",
title_cancel="Exit me",
force_separate_button=True,
).add_to(m)
# Display the map
m.save('custom_legend_map.html')
st_folium(m, width= 700)