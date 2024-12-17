FROM python:3.12.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

RUN apt-get install git-lfs

RUN git lfs install

RUN git clone https://github.com/davnish/parcel_streamlit.git .

RUN git checkout crop_type

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118

RUN pip3 install transformers

RUN pip3 install matplotlib

RUN pip3 install geopandas

RUN pip3 install streamlit

RUN pip3 install leafmap

RUN pip3 install streamlit-vis-timeline

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install opencv-python

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]