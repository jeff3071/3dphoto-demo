from PIL import Image
import streamlit as st
import numpy as np
import requests
import io
import os
import time

# Download the fixed image
def convert_image(img: Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def repaint_image(image: Image) -> Image: 
    files = {
        'image': ("flower.png", convert_image(image), 'image/png'),
    }
    print('start')
    start = time.time()
    response = requests.post(
        f"{os.environ['inpaint3d_server']}/uploadimage/",
        files=files,
    )
    end = time.time()
    print(f"{end - start} seconds")

    return response.content

def image_resize(_image, image_height, image_width):
    max_width = 720
    max_height = 720
    if image_width / image_height > max_width / max_height:
        new_image = _image.resize((max_width, int(image_height * max_width / image_width)))
    else:
        new_image = _image.resize((int(image_width * max_height / image_height), max_height))
    return new_image


st.set_page_config(layout="wide", page_title="3d photo generator")
bg_image = st.file_uploader("Background image:", type=["jpg"])
st.markdown("\n")
col1, col2 = st.columns(2)

if bg_image is not None:
    image_upload = Image.open(bg_image)
    image = np.array(image_upload)
    
    resize_image = image_resize(image_upload, image.shape[0], image.shape[1])
    with col1:
        st.image(resize_image, caption="Original image")
        
    result_video = repaint_image(resize_image)
        
    with col2:
        st.video(result_video, format="video/mp4", start_time=0)

            
