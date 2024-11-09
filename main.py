import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import os
import glob


class base:
    def __init__(self, title_name, color_column, popup, 
                 aliases, path, legend_order = None, color_dict = None):
        
        self.hex = {'red':'#ff0000', 'green':'#00FF00' , 'blue':'#0000FF', 'yellow': '#FFFF00', 'orange': '#ffa500', 'black': '#000000', 'brown':'#5C4033', 'pink':'#FFC0CB'}

        if color_dict is None:
            self.color_dict = {'Low': 'red', 'High': 'green', 'Healthy': 'green', 'Moderate': 'blue', 
              'Blackgram': 'blue', 'Paddy': 'yellow', 'Soybean': 'green', 'No Claim': 'blue', 
              'No Data': 'black', 'Prevented Sowing': 'yellow', 'Yield Loss': 'red', 
              'Cotton': 'pink', 'Pearl Millet': 'brown', 'No crop': 'black', 'No': 'brown' , 
              'Pre-Harvest Loss': 'yellow', 'Localised Claim(Pest)': 'yellow', 'Claim data': 'yellow', 'No Calamity':'brown', 'Harvested': 'pink'}
        else:
            self.color_dict = color_dict
        
        # for i in self.color_dict.keys():
        #     self.color_dict[i] = hex[self.color_dict[i]]
        
        # print(color_dict)
        self.title_name = title_name
        self.color_column = color_column
        self.popup = popup
        self.aliases = aliases
        self.legend_order = legend_order
        self.path = path
        # if colormap is not None: self.colormap = colormap
        # else: self.colormap = cm.get_palette("Paired")
        # print(self.colormap) 

        logo_path = os.path.join("misc", "logo", "file-removebg-preview.png")
        sidebar_path = os.path.join("misc", "logo", "file-removebg-preview.png")

        st.logo(sidebar_path, icon_image=logo_path)
        st.sidebar.image(logo_path)

        st.title(f'{title_name}')

        if 'selected' not in st.session_state:
            st.session_state['selected'] = False

    def get_data(self, path):
        # print(path)
        gdf = gpd.read_file(path)
        return gdf

    def add_map(self, path, layer_name, color=None):
        if color is None:
            color = 'blue'

        line_style = {
            'color': color,      # Line color
            'weight': 4,          # Line thickness
            'dashArray': '7, 7',
            'fillOpacity': 0   # Creates a dashed effect: "5px line, 5px space"
        }

        gdf = gpd.read_file(path)
        self.m.add_gdf(gdf, style = line_style, layer_name = layer_name, info_mode=None)
        self.m.set_center(lat=gdf.geometry.centroid.y.mean(), lon=gdf.geometry.centroid.x.mean(), zoom=10)
        
    # This function is for read parcel amp
    def add_parcel_map(self ,path, legend_title=None):
        self.gdf = self.get_data(path)
        gdf_idx = self.gdf[self.color_column]

        if self.legend_order is None:
            legend_dict = {cate : self.hex[self.color_dict[cate]] for cate in sorted(gdf_idx.unique())}
        else:
            legend_dict = {cate : self.hex[self.color_dict[cate]] for cate in self.legend_order}
            
        
        color_dict = {key: legend_dict[gdf_idx[key]] for key in gdf_idx.keys()}

        style_function=lambda feature: {
            "fillColor": color_dict[int(feature['id'])],
            "color": "black",
            "weight": 1,
            "fillOpacity": 1,
        }
        
        if self.popup and self.aliases:
            for name, col in zip(self.aliases, self.popup):
                self.gdf.rename(columns = {col:name}, inplace = True)
            self.gdf = self.gdf.loc[:, [*self.aliases, 'geometry']]
        

        self.m.add_gdf(self.gdf, 
                       layer_name = f"{self.title_name}", zoom_on_click=True, 
                       style_function=style_function, 
                       highlight_function = lambda x: {'weight': 3, 'color': 'red'})
        
        if legend_title:

            self.m.add_legend(title=legend_title, legend_dict=legend_dict, draggable=False)
        else:
            self.m.add_legend(title=f"{self.title_name}", legend_dict=legend_dict, draggable=False)

        self.m.set_center(lat=self.gdf.geometry.centroid.y.mean(),lon=self.gdf.geometry.centroid.x.mean(), zoom = 15 )
    
        
    def set_map(self):
        # gdf = self.get_data(path)
        self.m = leafmap.Map(location = [22.176,78.410], zoom_start=5, draw_control=None)
        self.m.add_basemap("SATELLITE")
    
    def get_options_dir(self, path):
        return sorted([i.title() for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]) 
        # return sorted([i.title() for i in os.listdir(path)]) # This is edited to remove 2023 data

    @staticmethod
    def del_key(key):
        if key in st.session_state:
            del st.session_state[key]

    @staticmethod
    def store_values(key):
        if key == 'state_key': #This is done because if directly changes the selectbox without removing the selectbox
            base.del_key('district_key')
            base.del_key('tehsil_key')
            base.del_key('village_key')
            base.del_key('year_key')
            # base.del_key('district_key')


        st.session_state[key] = st.session_state['_'+key]

    # @staticmethod
    def load_keys(self, key):
        if key in st.session_state:
            if key == 'state_key':
                if st.session_state[key] in self.states_opt:
                    st.session_state['_'+key] = st.session_state[key]
                else: 
                    base.del_key(key)
                    base.del_key('district_key')
                    base.del_key('tehsil_key')
                    base.del_key('village_key')
                    base.del_key('year_key')
            elif key == 'year_key':
                if st.session_state[key] in self.year_opts:
                    st.session_state['_'+key] = st.session_state[key]
                else: 
                    base.del_key(key)

            else: st.session_state['_'+key] = st.session_state[key]
    
    def add_admin_path(self, selection):
        self.admin_path = os.path.join(self.admin_path, selection.lower()) # To be used to display admin bounds map

    def add_product_path(self, selection):
        self.path = os.path.join(self.path, selection.lower())

    def add_admin(self, idx, col, admin, options):        
        selection = None
        self.load_keys(f'{admin}_key')
        with col: 
                selection = st.selectbox(
                    
                    f"Select your {admin.title()}:", 
                    options,  
                    index = None, 
                    placeholder='Select', 
                    on_change=base.store_values, 
                    key = f'_{admin}_key', 
                    args=[f"{admin}_key"], 
                    disabled=not self.options_visibility[idx]

                    )
                
        return selection
    
    @staticmethod
    def get_key_value(key):
        key = key+'_key'
        if key in st.session_state:
            return st.session_state[key]
        
    
    def format(self):

        self.set_map()
        admin_list = ['state', 'district', 'tehsil', 'village', 'year']
        admin_bounds_color = ['#661100', '#6699CC', '#71035e', '#000000']

        grid = st.columns(len(admin_list))

        # Adding admin bounds
        self.admin_path = r'data/admin_bounds/state_boundary'
        self.options_visibility = [True, False, False, False, False] 
        
        
        for idx, admin in enumerate(admin_list):

            if admin == 'state':
                options = self.get_options_dir(self.path)
                self.states_opt = options # states_opt is for checking if the options given is available for the current product
            elif admin == 'year':
                options = self.get_options_dir(self.path)
                self.year_opts = options
            else:
                options = self.get_options_dir(self.admin_path)

            selection = self.add_admin(idx, grid[idx], admin, options)

            if selection: # if statments if the streamlit run being selection None
                if admin=='state' or admin == 'year': 
                    self.add_product_path(selection)
                
                if admin != 'year':
                    self.options_visibility[idx+1] = True
                    self.add_admin_path(selection)
                    self.add_map(self.get_filename(self.admin_path), admin.title(), admin_bounds_color[idx])
        
        self.year = base.get_key_value('year')
    
    def get_filename(self, path, extension='*.shp'):
        for i in glob.glob(os.path.join(path, extension)): return i
            

# --- Page Setup ---

crop_map = st.Page(
    page = "views/Crop_Map.py",
    title = "Crop Map",
    icon = "🗺️",
    default = True
)

yield_map = st.Page(
    page = "views/Yield.py",
    title = "Yield Map",
    icon = "🌾",
)

sowing_status = st.Page(
    page = "views/tillage_status.py",
    title = "Tillage Status",
    icon = "👨🏽‍🌾",
)

claims = st.Page(
    page = "views/Claims.py",
    title = "Claims",
    icon = "📊",
)

weather_data = st.Page(
    page = "views/weather_data.py",
    title = "Weather Data",
    icon = "🌤️",
)

chm = st.Page(
    page = "views/CHM.py",
    title = "Crop Health Monitoring",
    icon = "🌱"
)
# -- Setting Navigation --

pg = st.navigation(pages = [sowing_status, crop_map, chm, yield_map, claims, weather_data])

# -- Run Nav --

pg.run()