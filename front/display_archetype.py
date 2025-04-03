import streamlit as st
from pathlib import Path
from streamlit_extras.tags import tagger_component


def display_archetype(name: str, img_path: str | Path, palette_path: str | Path, description : str, tags: list[str]):
    st.title(name)

    c1, c2  = st.columns(2)
    with c1:
        st.image(img_path)
        st.image(palette_path)


    with c2:
        st.write("Description")
        st.write(description)
        tagger_component("Tag:  \n", tags)