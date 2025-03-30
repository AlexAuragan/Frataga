import os
import boto3
from botocore.client import Config
from tqdm import tqdm
import tempfile
from main import get_palette, find_color_palette
from scripts.utils import name_to_key

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_USER"),
    aws_secret_access_key=os.environ.get("MINIO_PASSWORD"),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def send_to_db(bucket_name: str, project_name: str):
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
                s3.upload_file(img_path, bucket_name, f"{project_name}/{name_to_key(folder)}.png")
                palette = get_palette(find_color_palette(img_path))
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    palette.save(tmp.name)
                    s3.upload_file(tmp.name, bucket_name, f"{project_name}_palette/{name_to_key(folder)}.png")
                os.remove(tmp.name)

if __name__ == '__main__':
    bucket_name = "archetypes"
    project_name = "frataga"

    send_to_db(bucket_name, project_name)
