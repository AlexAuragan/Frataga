import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("Frataga")
        st.selectbox(options=["frataga", "greek_gods"], index=1, key="collection", label="Collection sélectionnée",
                     format_func=lambda x: {"frataga": "Frataga", "greek_gods": "Greek Gods"}[x])
        st.page_link("main.py", label="Accueil", icon=":material/home:")
        st.page_link("pages/gallery.py", label="Gallerie", icon=":material/gallery_thumbnail:")
        st.divider()
        st.page_link("pages/about.py", label="À propos", icon=":material/info:")