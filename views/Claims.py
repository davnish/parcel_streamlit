import streamlit as st
import os
from main import base
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")


class claims_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path):
        super().__init__(title_name, color_column, popup, aliases, path)

    def get_path(self):
        crops = []
        if self.year: crops.extend(self.get_options_dir())
        self.crop_type = st.selectbox("Select your Crop", crops, index = None, placeholder='Select', key = 'crop_type')

        if self.crop_type: 
            self.path = os.path.join(self.path, self.crop_type.lower())
            # self.path = self.get_filename()
        
        return self.path

    def __call__(self):
        self.format()
        path = self.get_path()
        # print(path)

        if 'claims_radio_visibility' not in st.session_state or not st.session_state['crop_type']:
            st.session_state['claims_radio_visibility'] = True

        loss_list = ["Yield_Loss", "Localised_Calamities", "Prevented_Sowing", "Crop_Loss"]

        index = None
        if st.session_state['crop_type']:
            loss_list_have = self.get_options_dir()
            # index = np.isin(loss_list, loss_list_have)
            # index = int(np.where(index == True)[0][0])
            self.del_key('claims_radio_visibility')
            st.session_state['claims_radio_visibility'] = False
            
        claim = st.sidebar.radio("Select which data to see:", loss_list, index = None, disabled = st.session_state.claims_radio_visibility, key='claim')
        
        if claim:
            if claim not in loss_list_have:
                claim = None
        
        if claim:
            path = os.path.join(self.path, claim.lower())

            if claim == 'Yield_Loss':
                self.popup = ["Cause of L", 'Claims A_1', 'Yield Loss', 'Yield Lo_1']
                self.aliases = ['Type of Claim:', 'Claim Amount:', 'Yield Loss (Kg/ha)', 'Yield Loss Percentage']

            self.add_parcel_map(self.get_filename(path), legend_title=claim)
        self.m.to_streamlit(layout = 'wide')
        
        # side bar



title_name = 'Claims Data'
path = r'data/claims'
color_column = 'Cause of L'


popup = ["Cause of L", 'Claims A_1']
aliases = ['Cause of Loss:', 'Claim Amount:']

claims_map(title_name, color_column, popup, aliases, path)()

if 'state_key' in st.session_state and st.session_state['claim'] == 'Yield_Loss':
    if st.session_state['state_key'] == 'Haryana':
        st.divider()
        col = st.columns(4)

        with col[3]: st.write("Threshold Yield(IU): 360 kg/ha")


        with st.container():

            with open('style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

            st.subheader('AgronomIQ:')
            df = pd.read_csv('data/claims/haryana/2022/cotton/yield_loss/csv/agronomiq.csv')

            st.table(df)

            st.subheader('PMFBY:')
            df = pd.read_csv('data/claims/haryana/2022/cotton/yield_loss/csv/pmfby.csv')

            st.table(df)
            


    # st.table(column = , index = None)

