import os
import pandas as pd
from PIL import Image, ImageDraw
from Pylette import extract_colors, Color
import streamlit as st
import config
from scripts.utils import name_to_key
from vectorize import init_reduce_dims_model, arch_finder
from database import get_data_from_name, get_image_from_key
from dotenv import load_dotenv

load_dotenv()

def list_images() -> list[str]:
    return sorted(os.listdir("images"))

def get_image_path(archetype_name: str) -> str:
    safe_name = archetype_name.replace("'", "_")
    archetype_dir = os.path.join("images", safe_name)

    for filename in os.listdir(archetype_dir):
        if filename.endswith(".png"):
            return os.path.join(archetype_dir, filename)
    raise ValueError(f"Image {arch} not found in images ")

def find_color_palette(image_path: str) -> list[tuple[int, int, int]]:
    return [extract_colors(image=image_path, palette_size=8)[i].rgb for i in range(8)]


def get_palette(colors, padding=5):
    """
    Save a color palette as a PNG image.

    Parameters:
        colors (list of array-like): List of RGB colors (e.g., [array([R,G,B]), ...])

        padding (int): Padding between color blocks.
    """
    width = 1024
    cell_width = int((width - padding) / len(colors) - padding)
    cell_height = 128
    height = cell_height + 2 * padding

    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i, color in enumerate(colors):
        x0 = padding + i * (cell_width + padding)
        y0 = padding
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        draw.rectangle([x0, y0, x1, y1], fill=color)

    return img


if __name__ == '__main__':
    with st.spinner("Starting server..."):
        model = init_reduce_dims_model()

    st.title("DnD archetype search")
    df = pd.read_json("data_format.json").T


    vectors_dict = {}
    for arch in df.index:
        value = arch
        key = df.loc[arch][f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS}"]
        vectors_dict[tuple(key)] = value


    desc = st.text_input("Prompt", placeholder="J'aime la nature et la musique.")
    with st.spinner(""):
        match = arch_finder(desc, vectors_dict, model)
        key = name_to_key(match)
        data = get_data_from_name(key)
        img_path = get_image_from_key(data["minio_key"])

    st.title(match)
    st.image(img_path)

    st.image(os.path.join("palettes", match + ".png"))
    c1, c2  = st.columns(2)
    with c1:
        st.write("Description")
        st.write(df.loc[match]["description_fr"])

    with c2:
        st.write("Tags:")
        st.write(df.loc[match]["tags_fr"])