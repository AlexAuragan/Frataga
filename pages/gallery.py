from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st

from database import get_image_from_key, get_data_from_name, get_db_dict
from front.sidebar import sidebar

def gallery():
    nb_col = 4
    collection = st.session_state["collection"]
    keys_to_names = get_db_dict("name", collection)
    all_images = {}
    with st.spinner(""):
        with ThreadPoolExecutor() as executor:
            future_to_name = {
                executor.submit(get_image_from_key, get_data_from_name(key)["picture_minio_key"]): name
                for name, key in keys_to_names.items()
            }

            for future in as_completed(future_to_name):
                name = future_to_name[future]
                img_path = future.result()
                all_images[name] = img_path

    columns = st.columns(nb_col)
    for i, (name, img) in enumerate(all_images.items()):
        c = columns[i % nb_col]
        with c:
            st.header(name)
            st.image(img)

if __name__ == '__main__':
    sidebar()
    gallery()
