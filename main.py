import streamlit as st
import config
from front.gallery_tab import gallery_tab
from front.prompt_tab import prompt_tab
from front.sidebar import sidebar
from vectorize import init_reduce_dims_model
from database import get_db_dict
from dotenv import load_dotenv
import sys
from streamlit_extras.bottom_container import bottom
from front.selection_tab import selection_tab

# Avoid the issue between streamlit watcher and torch.classes
sys.modules['torch.classes'].__path__ = []
# Load environment variable
load_dotenv()

st.set_page_config(layout="wide")

def footer():
    with bottom():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.link_button("source code", "https://github.com/AlexAuragan/Frataga")
        with c2:
            st.link_button("MIT License", "https://github.com/AlexAuragan/Frataga/blob/master/LICENSE")
        with c2:
            st.write("")
        with c4:
            st.write("Made with love by [AlexAuragan](https://github.com/AlexAuragan) and [Aurizon128](https://github.com/Aurizon128/)", unsafe_allow_html=True)

if __name__ == '__main__':
    sidebar()
    collection = st.session_state["collection"]
    with st.spinner("Starting server..."):
        model = init_reduce_dims_model(collection)

    t1, t2 = st.tabs(["Recherche", "Selection"])
    footer()


    with t1:
        field = f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS[collection]}"
        vectors_dict = get_db_dict(field, collection)
        assert vectors_dict
        prompt_tab(vectors_dict=vectors_dict, model=model)

    with t2:
        keys_to_names = get_db_dict("name", collection)
        selection_tab(keys_to_names)

    # with t3:
    #     keys_to_names = get_db_dict("name", collection)
    #     gallery_tab(keys_to_names)