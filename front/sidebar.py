import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("Frataga")
        st.page_link("main.py", label="Accueil", icon=":material/home:")
        st.divider()
        st.page_link("pages/about.py", label="À propos", icon=":material/info:")
