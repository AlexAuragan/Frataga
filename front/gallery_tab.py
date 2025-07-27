import concurrent
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

from database import get_image_from_key, get_data_from_name


@st.fragment
def gallery_tab(names_to_keys: dict) -> None:

    all_images = {}
    with st.spinner(""):
        with ThreadPoolExecutor() as executor:
            future_to_name = {
                executor.submit(get_image_from_key, get_data_from_name(key)["picture_minio_key"]): name
                for name, key in names_to_keys.items()
            }

            for future in concurrent.futures.as_completed(future_to_name):
                name = future_to_name[future]
                img_path = future.result()
                all_images[name] = img_path

    c1, c2 = st.columns(2)
    for i, (name, img) in enumerate(all_images.items()):
        c = c1 if (i % 2 == 0) else c2
        with c:
            st.header(name)
            st.image(img)

