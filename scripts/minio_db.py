import os
import boto3
from botocore.client import Config

from scripts.utils import name_to_key

bucket_name = "archetypes"
project_name = "frataga"

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_USER"),
    aws_secret_access_key=os.environ.get("MINIO_PASSWORD"),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def send_to_db():
    """
    send images that are in folders like
    images/
     |_ Archetype_1/
            |_ image.png

    we do this because we found it's easier to download Midjourney images and put them into corresponding folder
    than renaming them one by one

    """
    for folder in os.listdir("images"):
        for img in os.listdir(os.path.join("images", folder)):
            if img.endswith(".png"):
                s3.upload_file(os.path.join("images", folder, img), bucket_name, f"{project_name}/{name_to_key(folder)}.png")

def get_from_db():
    """
    Download images like
    images/
        |_ archetype_1.png


    """
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{project_name}/")
    for obj in response.get('Contents', []):
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": obj["Key"]},
            ExpiresIn=3600
        )

if __name__ == '__main__':
    # send_to_db()
    get_from_db()