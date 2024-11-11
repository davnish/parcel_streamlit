import streamlit as st
import os
from main import base
import numpy as np

st.set_page_config(layout="wide")


class claims_map(base):
    def __init__(self, title_name, color_column, popup, aliases, path):
        super().__init__(title_name, color_column, popup, aliases, path)

    def get_path(self):
        crops = []
        if self.year: crops.extend(self.get_options_dir(self.path))
        self.crop_type = st.selectbox("Select your Crop", crops, index = None, placeholder='Select', key = 'crop_type')

        if self.crop_type: 
            self.path = os.path.join(self.path, self.crop_type.lower())
            # self.path = self.get_filename()
        
        return self.path

    def __call__(self):
        self.format()
        path = self.get_path()
        # print(path)

        if 'claims_radio_visibility' not in st.session_state:
            st.session_state['claims_radio_visibility'] = True

        loss_list = ["Localised_Calamities", "Yield_Loss", "Prevented_Sowing", "Crop_Loss"]


        index = None
        if self.crop_type:
            loss_list_have = self.get_options_dir(path)
            index = np.isin(loss_list, loss_list_have)
            index = int(np.where(index == True)[0][0])
            st.session_state['claims_radio_visibility'] = False
            
        claim = st.sidebar.radio("Select which data to see:", loss_list, index = index, disabled = st.session_state.claims_radio_visibility)
        
        if claim:
            if claim not in loss_list_have:
                claim = None
        
        if claim:
            path = os.path.join(path, claim.lower())

            if claim == 'Yield_Loss':
                self.popup = ["Cause of L", 'Claims A_1', 'Yield Loss', 'Yield Lo_1']
                self.aliases = ['Cause of Loss:', 'Claim Amount:', 'Yield Loss (Kg/ha)', 'Yield Loss Percentage']

            self.add_parcel_map(self.get_filename(path), legend_title=claim)
        self.m.to_streamlit(layout = 'wide')
        
        # side bar



title_name = 'Claims Data'
path = r'data/claims'
# colormap = ["#FF0000", "#00FF00", "#0000FF"]
color_column = 'Cause of L'


popup = ["Cause of L", 'Claims A_1']
aliases = ['Cause of Loss:', 'Claim Amount:']

claims_map(title_name, color_column, popup, aliases, path)()

st.divider()

col = st.columns(3)
col[0].metric("Indemnity Level:", "80 %") 
col[1].metric("Threshold Yield(IU):", "360 kg/ha")
col[2].metric("Average Acutal Yield(IU):", "298.8 kg/ha")

col2 = st.columns(3)
# col2[0].metric("Estimated Average Actual Yield(Parcelwise):", "259.87 kg/ha")
col2[0].metric("Model Yield For IU At Parcel Level", "259.87 kg/ha")
col2[1].metric("Estimated Claim(Sum):", "₹ 13,70,937")
# col2[2].metric("Suggested Yield By TIP", "189.19 kg/ha") # Need to change this
col2[2].metric("Model Yield For IU At Village Level", "189.19 kg/ha") # Need to change this

# st.table(column = , index = None)

