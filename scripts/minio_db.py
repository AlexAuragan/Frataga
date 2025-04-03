import os
import boto3
from PIL import Image, ImageDraw
from botocore.client import Config
from tqdm import tqdm
import tempfile
from Pylette import extract_colors

from scripts.utils import name_to_key

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_USER"),
    aws_secret_access_key=os.environ.get("MINIO_PASSWORD"),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)
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

def send_to_db(bucket_name: str, series_name: str):
    """
    send images that are in folders like
    images/
     |_ Archetype_1/
            |_ image.png

    we do this because we found it's easier to download Midjourney images and put them into corresponding folder
    than renaming them one by one

    """
    for folder in tqdm(os.listdir("images")):
        for img in os.listdir(os.path.join("images", folder)):
            if img.endswith(".png"):
                img_path = os.path.join("images", folder, img)
                s3.upload_file(img_path, bucket_name, f"{series_name}/{name_to_key(folder)}.png")
                palette = get_palette(find_color_palette(img_path))
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    palette.save(tmp.name)
                    s3.upload_file(tmp.name, bucket_name, f"{series_name}_palette/{name_to_key(folder)}.png")
                os.remove(tmp.name)

if __name__ == '__main__':
    _bucket_name = "archetypes"
    _series_name = "frataga"

    send_to_db(_bucket_name, _series_name)
