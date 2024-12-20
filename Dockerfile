# FROM python:3.12.8-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

# # RUN apt-get install git-lfs

# # RUN git lfs install

# # RUN git clone https://github.com/davnish/parcel_streamlit.git .

# # RUN git checkout crop_type

# COPY . .

# RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# RUN pip3 install transformers

# RUN pip3 install matplotlib

# RUN pip3 install geopandas

# RUN pip3 install streamlit

# RUN pip3 install leafmap

# RUN pip3 install streamlit-vis-timeline

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# RUN pip3 install opencv-python

# EXPOSE 8501

# ENTRYPOINT ["streamlit", "run", "main.py"]

FROM python:3.12.8-slim

# Set working directory
WORKDIR /app

# Install required system packages in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Git LFS
# RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
#     apt-get install -y git-lfs && \
#     git lfs install

# Clone the repository and checkout the desired branch
# RUN git clone --branch crop_type https://github.com/davnish/parcel_streamlit.git .
COPY . .

# Install Python dependencies in a single command for caching
RUN pip3 install --no-cache-dir  torch torchvision --index-url https://download.pytorch.org/whl/cu118 

RUN pip3 install --no-cache-dir \
    transformers \
    matplotlib \
    geopandas \
    streamlit \
    leafmap \
    streamlit-vis-timeline \
    opencv-python

# Expose Streamlit's default port
EXPOSE 8501

# Set the entry point
ENTRYPOINT ["streamlit", "run", "main.py"]
