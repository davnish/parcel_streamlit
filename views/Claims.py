import streamlit as st
import os
from util import base
import pandas as pd

if 'setting_page' not in st.session_state:
    st.set_page_config(layout="wide")
    st.session_state['setting_page'] = True


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
        loss_list_have = None
        index = None
        if st.session_state['crop_type']:
            loss_list_have = self.get_options_dir()
            # index = np.isin(loss_list, loss_list_have)
            # index = int(np.where(index == True)[0][0])
            self.del_key('claims_radio_visibility')
            st.session_state['claims_radio_visibility'] = False
            
        claim = st.sidebar.radio("Select which data to see:", loss_list, index = None, disabled = st.session_state.claims_radio_visibility, key='claim')
        
        if claim:
            if not loss_list_have or claim not in loss_list_have :
                claim = None
        
        if claim:
            path = os.path.join(self.path, claim.lower())
            legend_order = None
            if claim == 'Yield_Loss':
                self.popup = ["Cause of L", 'Claims A_1', 'Yield Loss', 'Yield Lo_1']
                self.aliases = ['Type of Claim:', 'Claim Amount:', 'Yield Loss (Kg/ha)', 'Yield Loss Percentage']

                if st.session_state['state_key'] == 'Haryana':
                    legend_order = ["Yield loss", "NoYield loss"]
                elif st.session_state['state_key'] == 'Madhya_Pradesh':
                    legend_order = ["No Claim", "Yield Loss"]

            self.add_parcel_map(self.get_filename(path), legend_title=claim, legend_order=legend_order)
        self.m.to_streamlit(layout = 'wide')
        
        # side bar



title_name = 'Claims Data'
path = r'data/claims'
color_column = 'Cause of L'


popup = ["Cause of L", 'Claims A_1']
aliases = ['Cause of Loss:', 'Claim Amount:']

claims_map(title_name, color_column, popup, aliases, path)()


def show_tb(th, tr, show_svg = False):
    if show_svg:
        svg_icon = """<svg xmlns="http://www.w3.org/2000/svg" height="20" width="15" viewBox="0 0 384 600"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="#11ff00" d="M169.4 470.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 370.8 224 64c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 306.7L54.6 265.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>"""
        table_html = f"""<table data-testid="stTableStyledTable" class="st-emotion-cache-zuelfj e1q9reml3"><thead><tr><th class="blank st-emotion-cache-c34i5s e1q9reml1">&nbsp;</th><th scope="col" class="col_heading level0 col0 st-emotion-cache-c34i5s e1q9reml1" style="text-align: left;">
        {th[0]}</th><th scope="col" class="col_heading level0 col1 st-emotion-cache-c34i5s e1q9reml1" style="text-align: left;">
        {th[1]}</th><th scope="col" class="col_heading level0 col2 st-emotion-cache-c34i5s e1q9reml1" style="text-align: left;">
        {th[2]}</th></tr></thead><tbody><tr><th scope="row" class="row_heading level0 row0 st-emotion-cache-c34i5s e1q9reml1">0</th><td class="st-emotion-cache-4sszyo e1q9reml2" style="text-align: left;">
        {tr[0]}</td><td class="st-emotion-cache-4sszyo e1q9reml2" style="text-align: left;">
        {tr[1]}</td><td class="st-emotion-cache-4sszyo e1q9reml2" style="text-align: left;">
        {tr[2]}, ({svg_icon} {tr[3]} Lakhs, {tr[4]})</td></tr></tbody></table>"""

    else:
        table_html = f"""<table data-testid="stTableStyledTable" class="st-emotion-cache-zuelfj e1q9reml3"><thead><tr><th class="blank st-emotion-cache-c34i5s e1q9reml1">&nbsp;</th><th scope="col" class="col_heading level0 col0 st-emotion-cache-c34i5s e1q9reml1" style="text-align: left;">{th[0]}</th><th scope="col" class="col_heading level0 col1 st-emotion-cache-c34i5s e1q9reml1" style="text-align: left;">{th[1]}</th><th scope="col" class="col_heading level0 col2 st-emotion-cache-c34i5s e1q9reml1" style="text-align: left;">{th[2]}</th></tr></thead><tbody><tr><th scope="row" class="row_heading level0 row0 st-emotion-cache-c34i5s e1q9reml1">0</th><td class="st-emotion-cache-4sszyo e1q9reml2" style="text-align: left;">{tr[0]}</td><td class="st-emotion-cache-4sszyo e1q9reml2" style="text-align: left;">{tr[1]}</td><td class="st-emotion-cache-4sszyo e1q9reml2" style="text-align: left;">{tr[2]}</td></tr></tbody></table>"""

    st.markdown(table_html, unsafe_allow_html=True)


if 'state_key' in st.session_state and 'year_key' in st.session_state and st.session_state['claim'] == 'Yield_Loss':
    th_1 = ['Modeled Average Yield for IU (Parcel Level)', 'Yield Loss Percentage', 'Claim Amount (Estimated)']
    th_2 = ['Government Average Yield For IU', 'Yield Loss Percentage', 'Claim Amount (Settled)']
    st.divider()
    with open('style.css') as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 
    
    if st.session_state['state_key'] == 'Haryana' and st.session_state['year_key'] == '2022':
        col = st.columns(4)
        with col[3]: st.write("Threshold Yield(IU): 360 kg/ha")


        with st.container():
            st.subheader('AgronomIQ:')
            tr_1 = ['319.621 Kg/ha', '13.48%', '19.32 Lakhs', '5.41', '21%']
            show_tb(th_1, tr_1, show_svg=True)  

            st.subheader('PMFBY:')
            
            df = pd.read_csv('data/claims/haryana/2022/cotton/yield_loss/csv/pmfby.csv')
            st.table(df)
        
    elif st.session_state['state_key'] == 'Madhya_Pradesh' and st.session_state['year_key'] == '2022':
        col = st.columns(4)

        with col[3]: st.write("Threshold Yield(IU): 533 kg/ha")

        with st.container():

            st.subheader('AgronomIQ:')
            tr_1 = ['446.62 Kg/ha', '16.29%', '	8,12,409 Lakhs', '1.65', '16%']
            show_tb(th_1, tr_1, show_svg=True)

            st.subheader('PMFBY:')

            df = pd.read_csv('data/claims/madhya_pradesh/2022/soybean/yield_loss/csv/pmfby.csv')
            st.table(df)