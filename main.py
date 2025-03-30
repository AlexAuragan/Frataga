import concurrent.futures
import os
import pandas as pd
from PIL import Image, ImageDraw
from Pylette import extract_colors
import streamlit as st
import config
from scripts.utils import name_to_key
from vectorize import init_reduce_dims_model, arch_finder
from database import get_data_from_name, get_image_from_key, get_palette_from_key, get_vectors_dict
from dotenv import load_dotenv
import sys

# Avoid the issue between streamlit watcher and torch.classes
sys.modules['torch.classes'].__path__ = []

# Load environment variable
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
        color = tuple(color)
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

    field = f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS}"
    vectors_dict = get_vectors_dict(field)

    desc = st.text_input("Prompt", placeholder="J'aime la nature et la musique.")
    with st.spinner(""):
        match = arch_finder(desc, vectors_dict, model)
        key = name_to_key(match)
        data = get_data_from_name(key)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_img = executor.submit(get_image_from_key, data["minio_key"])
            future_palette = executor.submit(get_palette_from_key, data["minio_key"])

            img_path = future_img.result()
            palette_path = future_palette.result()

    st.title(data["name"])
    st.image(img_path)
    st.image(palette_path)
    c1, c2  = st.columns(2)
    with c1:
        st.write("Description")
        st.write(data["description_fr"])

    with c2:
        st.write("Tags:")
        st.write(data["tags_fr"])