import concurrent.futures
from typing import Union, TYPE_CHECKING

import streamlit as st


from database import get_data_from_name, get_image_from_key, get_palette_from_key
from scripts.utils import name_to_key
from vectorize import arch_finder

def selection_tab(names_to_keys: dict) -> None:

    name = st.selectbox("Archetypes",options=names_to_keys.keys())
    with st.spinner(""):
        data = get_data_from_name(names_to_keys[name])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_img = executor.submit(get_image_from_key, data["picture_minio_key"])
            future_palette = executor.submit(get_palette_from_key, data["palette_minio_key"])

            img_path = future_img.result()
            palette_path = future_palette.result()

    st.title(data["name"])
    st.image(img_path)
    st.image(palette_path)
    c1, c2  = st.columns(2)
    with c1:
        st.write("Description")
        st.write(data["description_fr"])

    with c2:
        st.write("Tags:")
        st.write(data["tags_fr"])

