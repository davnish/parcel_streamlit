import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import os
import glob
import random
import toml

class base:
    def __init__(self, title_name, color_column, popup, 
                 aliases, path, legend_order = None, color_dict = None):
        
        self.hex = {'red':'#ff0000', 'green':'#00FF00' , 'blue':'#0000FF', 'yellow': '#FFFF00', 
                    'orange': '#ffa500', 'black': '#000000', 'brown':'#5C4033', 'pink':'#FFC0CB', 'light_green': '#D1FFBD', 'dark_green': '#006400'}
        

        if color_dict is None:
            self.color_dict_toml = toml.load('color_dict.toml')
        
            self.color_dict ={**self.color_dict_toml["crop_colors"], **self.color_dict_toml['crop_health'], **self.color_dict_toml['claims'], **self.color_dict_toml['misc']}
        else:
            self.color_dict = color_dict

        self.title_name = title_name
        self.color_column = color_column
        self.popup = popup
        self.aliases = aliases
        self.legend_order = legend_order
        self.path = path

        logo_path = os.path.join("misc", "logo", "image.png")
        sidebar_path = os.path.join("misc", "logo", "agronomiq.png")

        st.logo(sidebar_path, icon_image=logo_path, size = 'large')
        st.sidebar.image(logo_path)

        st.title(f'{title_name}')

        if 'selected' not in st.session_state:
            st.session_state['selected'] = False
        
    # @staticmethod
    def save_color_dict(self, cate, color):
        # color_dict = toml.load('color_dict.toml')
        self.color_dict_toml['misc'][cate] = color

        with open('color_dict.toml', 'w') as f:
            toml.dump(self.color_dict_toml, f)

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
    def add_parcel_map(self ,path, legend_title=None, crop_type=None, legend_order = None):
        if legend_order is not None:
            self.legend_order = legend_order
            
        self.gdf = self.get_data(path)
        gdf_idx = self.gdf[self.color_column]

        for cate in gdf_idx.unique():
            if cate not in self.color_dict.keys():
                color = random.choice(list(self.hex.keys()))
                self.color_dict[cate] = color
                self.save_color_dict(cate, color)

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

        if crop_type:
            self.gdf  = self.gdf[self.gdf[f'{self.year}_Crop'] == crop_type]
        
        if self.popup and self.aliases:
            for name, col in zip(self.aliases, self.popup):
                self.gdf.rename(columns = {col:name}, inplace = True)
            self.gdf = self.gdf.loc[:, [*self.aliases ,'geometry']]
        

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
    
    def get_options_dir(self, admin=None):
        if admin == None:
            path = self.path
        elif admin == 'state' or admin == 'year':
            path = self.path
        elif admin == 'season':
            return ['Kharif']
        else:
            path = self.admin_path
        
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
            base.del_key('season_key')
            # base.del_key('district_key')


        st.session_state[key] = st.session_state['_'+key]

    # @staticmethod
    def load_keys(self, key):
        if key in st.session_state:
            if key == 'state_key':
                if st.session_state[key] in self.options: # This condition is to check if the state doesnt exists in the key it will delete all the related fields
                    st.session_state['_'+key] = st.session_state[key]
                else: 
                    base.del_key(key)
                    base.del_key('district_key')
                    base.del_key('tehsil_key')
                    base.del_key('village_key')
                    base.del_key('year_key')
            elif key == 'year_key':
                if st.session_state[key] in self.options:
                    st.session_state['_'+key] = st.session_state[key]
                else: 
                    base.del_key(key)
                    base.del_key('season_key')

            else: st.session_state['_'+key] = st.session_state[key]
    
    def add_admin_path(self, selection):
        self.admin_path = os.path.join(self.admin_path, selection.lower()) # To be used to display admin bounds map

    def add_product_path(self, selection):
        self.path = os.path.join(self.path, selection.lower())

    def add_admin(self, idx, col, admin, options, options_visibility):        
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
                    disabled=not options_visibility[idx]

                    )
                
        return selection
    
    @staticmethod
    def get_key_value(key):
        key = key+'_key'
        if key in st.session_state:
            return st.session_state[key]
        
        # return None
        
    
    def format(self):

        self.set_map()
        admin_list_1 = ['state', 'district', 'tehsil', 'village']
        admin_bounds_color = ['#661100', '#6699CC', '#71035e', '#000000']

        admin_list_2 = ['season', 'year']

        grid_1 = st.columns(len(admin_list_1))
        grid_2 = st.columns(len(admin_list_2))

        # Adding admin bounds
        self.admin_path = r'data/admin_bounds/state_boundary'
        self.options_visibility_1 = [True, False, False, False] 
        self.options_visibility_2 = [False, False]
        
        
        for idx, admin in enumerate(admin_list_1):

            self.options = self.get_options_dir(admin)

            selection = self.add_admin(idx, grid_1[idx], admin, self.options, options_visibility=self.options_visibility_1)

            if selection: # if statments if the streamlit run being selection None
                if admin=='state': 
                    self.add_product_path(selection)
                
                if idx<len(self.options_visibility_1)-1:
                    self.options_visibility_1[idx+1] = True

                else: self.options_visibility_2[idx - (len(self.options_visibility_1)-1)] = True
                self.add_admin_path(selection)
                self.add_map(self.get_filename(self.admin_path), admin.title(), admin_bounds_color[idx])
        
        for idx, admin in enumerate(admin_list_2):
            self.options = self.get_options_dir(admin)

            selection = self.add_admin(idx, grid_2[idx], admin, self.options, options_visibility=self.options_visibility_2)

            if selection: # if statments if the streamlit run being selection None
                if admin == 'year': 
                    self.add_product_path(base.get_key_value('year'))
                
                if idx<len(self.options_visibility_2)-1:
                    self.options_visibility_2[idx+1] = True
        
        self.year = base.get_key_value('year')
    
    def get_filename(self, path, extension='*.shp'):
        for i in glob.glob(os.path.join(path, extension)): return i