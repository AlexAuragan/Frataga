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
def get_palette_url_from_key(key: str, bucket_name: str = None):
    bucket_name = bucket_name or _bucket_name
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=3600
    )
    return url


def get_url_from_key(key: str, bucket_name: str = None):
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

@lru_cache(maxsize=64)
def get_palette_from_key(key: str):
    url = get_palette_url_from_key(key)
    response = requests.get(url)
    return Image.open(BytesIO(response.content))



def get_all_archetypes(meilisearch_index: str = None) -> set[str]:
    def document_keys_generator(index, batch_size=100):
        offset = 0
        seen_keys = set()
        while True:
            documents = index.get_documents(parameters={"limit":batch_size, "offset":offset})
            if not documents:
                break
            for doc in documents:
                new_keys = set(doc.keys()) - seen_keys
                if new_keys:
                    seen_keys.update(new_keys)
                    yield new_keys
            offset += batch_size
    meilisearch_index = meilisearch_index or _meilisearch_index
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    index = client.index(meilisearch_index)

    all_keys = set()
    for new_keys in document_keys_generator(index):
        print(f"New keys found: {new_keys}")
        all_keys.update(new_keys)
    return all_keys

@lru_cache()
def get_db_dict(field: str, meilisearch_index: str = None):
    def field_to_doc_generator(batch_size=100):
        offset = 0
        while True:
            documents = index.get_documents(parameters={"limit":batch_size, "offset":offset}).results
            if not documents:
                break

            for doc in documents:
                doc = dict(doc)
                if field in doc:
                    key = doc[field]
                    if isinstance(key, list):
                        key = tuple(key)
                    yield {key: doc["id"]}
                else:
                    raise KeyError(f"Field '{field}' not found in document: {doc}")

            offset += batch_size
    meilisearch_index = meilisearch_index or _meilisearch_index
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    index = client.index(meilisearch_index)
    field_dict = dict()
    for new_keys in field_to_doc_generator():
        for key, val in new_keys.items():
            field_dict[key] = val
    return field_dict

def get_data_from_name(name: str, meilisearch_index: str = None) -> dict:
    meilisearch_index = meilisearch_index or _meilisearch_index
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    index = client.index(meilisearch_index)

    return dict(index.get_document(name))

