import os
import boto3
from botocore.client import Config
import meilisearch
from dotenv import load_dotenv
from functools import lru_cache
from PIL import Image
import requests
from io import BytesIO

load_dotenv()
_bucket_name = "archetypes"
_meilisearch_index = "archetypes"

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_USER"),
    aws_secret_access_key=os.environ.get("MINIO_PASSWORD"),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def get_url_from_key(key: str, bucket_name = None):
    bucket_name = bucket_name or _bucket_name
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=3600
    )
    return url

@lru_cache(maxsize=64)
def get_image_from_key(key: str):
    url = get_url_from_key(key)
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def get_data_from_name(name: str, meilisearch_index: str = None) -> dict:
    meilisearch_index = meilisearch_index or _meilisearch_index
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    index = client.index(meilisearch_index)
    return dict(index.get_document(name))

