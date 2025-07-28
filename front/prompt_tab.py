import concurrent.futures
import random
import re
from pprint import pprint
from typing import Union, TYPE_CHECKING
from random import sample
import streamlit as st

from database import get_data_from_name, get_image_from_key, get_palette_from_key
from scripts.utils import name_to_key
from vectorize import arch_finder
from front.display_archetype import display_archetype

if TYPE_CHECKING:
    from umap import UMAP
    from sklearn.decomposition import PCA

demo_prompts = {"frataga": [
    "J'aime la nature et la musique.",
    "J'aime la vitesse et la discretion.",
    "J'aime la terre et le travail bien fait.",
    "J'aime danser et manger !",
    "J'aime explorer la nature",
    "Brûlez dans les Enfers !",
    "Je manipule mes ennemis.",
    "J'ai beaucoup trop souffert pour arrêter de me battre.",
    "Je suis tellement sombre que j'ai un corbeau de compagnie.",
    "Je veux découvrir tous les secrets du désert.",
],
    "greek_gods": [
        "J'aime l'océan et ses mystères infinis.",
        "J'aime la guerre, le sang et la gloire.",
        "J'aime la lumière, l'art et la vérité.",
        "J'aime les ruses et les mensonges." ,
        "J'aime la sagesse et les stratégies parfaites.",
        "J'aime les fêtes, le vin et la folie." ,
        "J'aime l’amour et tout ce qui est beau.",
        "J'aime protéger la famille et la maison.",
        "J'aime la nature sauvage et la chasse." ,
    ]
}
def next_demo_prompt(collection: str):
    st.session_state["demo_id"] = st.session_state.get("demo_id", random.randint(0, len(demo_prompts[collection]))) + 1

@st.fragment
def prompt_tab(vectors_dict: dict, model: Union["UMAP", "PCA"], collection: str) -> None:
    if "demo_id" not in st.session_state:
        st.session_state["demo_id"] = random.randint(0, len(demo_prompts[collection]))

    demo_id = st.session_state["demo_id"]
    c1, c2 = st.columns([7, 1])
    with c1:
        print(demo_id)
        desc = st.text_input(
            "Prompt",
            placeholder=demo_prompts[collection][demo_id % len(demo_prompts[collection])],
            help="Le prompt peut prendre la forme d'une description ou d'une réplique, inspirez-vous des exemples et "
                 "n'hésitez pas à explorer !"
        ) or demo_prompts[collection][demo_id % len(demo_prompts[collection])]
    with c2:
        st.text("")
        st.text("")
        st.button(label=":material/refresh:", on_click=lambda: next_demo_prompt(collection))
    with st.expander("Info:",expanded=False):
        st.text("Cette application a pour but de trouver le personnage qui correspond le mieux à votre prompte !\n"
                "Entrez une phrase pour décrire votre personnage et découvrez ce que notre IA à trouvé.\n\n"
                "L'IA étant basé sur des personnages de types DnD, elle a tendance à mieux fonctionner sur des phrases "
                "entières utilisant le champ lexical du fantastique.")
    with st.spinner(""):
        match = arch_finder(desc, vectors_dict, model)
        key = name_to_key(match)
        data = get_data_from_name(key)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_img = executor.submit(get_image_from_key, data["picture_minio_key"])
            future_palette = executor.submit(get_palette_from_key, data["palette_minio_key"])

            img_path = future_img.result()
            palette_path = future_palette.result()

    name = data.get("Titre (FR)", data["name"])
    sub_title = data.get("description wiki 1", "")
    sub_title = re.sub(r'\[\d+]', "", sub_title)
    sub_title = sub_title[0].upper() + sub_title[1:] if sub_title else ""
    description = data["description_fr"]
    tags = data["tags_fr"]
    display_archetype(name=name, description=description, tags=tags, img_path=img_path, palette_path=palette_path,
                      sub_title=sub_title)

