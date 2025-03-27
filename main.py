import os

import pandas as pd
from PIL import Image, ImageDraw
from Pylette import extract_colors, Color
import streamlit as st

import config
from vectorize import init_reduce_dims_model, arch_finder


def list_images():
    return sorted(os.listdir("images"))

def get_image_path(arch: str) -> str:
    arch = arch.replace("'", "_")
    arch_dir = os.path.join("images", arch)
    for img in os.listdir(arch_dir):
        if img.endswith(".png"):
            return os.path.join(arch_dir, img)
    raise ValueError(f"Image {arch} not found in images ")

def find_color_palette(img_path) ->list[Color]:
    return [extract_colors(image=img_path, palette_size=8)[i].rgb for i in range(8)]


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

    img = Image.new("RGB", (width, height + 2*padding), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i, color in enumerate(colors):
        x0 = padding + i * (cell_width + padding)
        y0 = padding
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        print(color)
        draw.rectangle([x0, y0, x1, y1], fill=tuple(color))
    return img

if __name__ == '__main__':
    all_arch = list_images() # liste tous les archetypes
    st.title("test streamlit")
    # selectbox prend une liste, et m'affiche un truc pour sélectionner dans la liste
    # arch = st.selectbox("Archetype selection",all_arch)
    model = init_reduce_dims_model()
    df = pd.read_json("data_format.json").T #.T inverse les lignes et les colones
    #print(df.head())
    #print(df.columns)

    vectors_dict = {}
    for arch in df.index:
        value = arch
        key = df.loc[arch][f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS}"]
        vectors_dict[tuple(key)] = value


    desc = st.text_input("Prompt", placeholder="J'aime la nature et la musique.")
    match = arch_finder(desc, vectors_dict, model)

    img_path = get_image_path(match)
    st.title(match)
    st.image(img_path)
    st.image(get_palette(find_color_palette(img_path)))
    c1, c2  = st.columns(2)
    with c1:
        st.write("Description")
        st.write(df.loc[match]["description_fr"])

    with c2:
        st.write("Tags:")
        st.write(df.loc[match]["tags_fr"])