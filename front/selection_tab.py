import concurrent.futures

import streamlit as st


from database import get_data_from_name, get_image_from_key, get_palette_from_key
from front.display_archetype import display_archetype

@st.fragment
def selection_tab(names_to_keys: dict) -> None:

    name = st.selectbox("Archetypes",options=names_to_keys.keys())
    with st.spinner(""):
        data = get_data_from_name(names_to_keys[name])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_img = executor.submit(get_image_from_key, data["picture_minio_key"])
            future_palette = executor.submit(get_palette_from_key, data["palette_minio_key"])

            img_path = future_img.result()
            palette_path = future_palette.result()

    name = data["name"]
    description = data["description_fr"]
    tags = data["tags_fr"]
    display_archetype(name=name, description=description, tags=tags, img_path=img_path, palette_path=palette_path)
