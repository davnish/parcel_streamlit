import streamlit as st
from transformers import pipeline
import numpy as np
from PIL import Image
import cv2


if 'setting_page' not in st.session_state:
    st.set_page_config(layout="wide")
    st.session_state['setting_page'] = True

st.title('Crop Identification')


option = st.segmented_control("Select Your Way", options=['Upload An Image', 'Click An Image'])

if option:

    classifier = pipeline("image-classification", model="vit_b_1",  device = 'cpu')

    if option == 'Click An Image':

        # enable = st.checkbox("Enable Camera")
        picture = st.camera_input("Take a picure")
    
    elif option == 'Upload An Image':


        picture = st.file_uploader("Choose an Image", accept_multiple_files=False, type = ['jpg','png'])
    
    if picture:
        st.write('uploaded')

        img = Image.open(picture)
        # bytes_data = picture.getvalue()
        # img = picture.getvalue()
        # img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR_RGB)
        st.image(img)
        reimg = np.asarray(img)
        # reimg = cv2.resize(reimg, (224, 224), interpolation = cv2.INTER_AREA)
        reimg = Image.fromarray(reimg)
        cls = classifier(reimg)
        st.write(cls)
        # st.image(picture)