import concurrent.futures
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

demo_prompts = [
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
]
def prompt_tab(vectors_dict: dict, model: Union["UMAP", "PCA"]) -> None:
    sample_prompt = sample(demo_prompts, 1)[0]
    desc = st.text_input("Prompt", placeholder=sample_prompt) or sample_prompt
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

    name = data["name"]
    description = data["description_fr"]
    tags = data["tags_fr"]
    display_archetype(name=name, description=description, tags=tags, img_path=img_path, palette_path=palette_path)

