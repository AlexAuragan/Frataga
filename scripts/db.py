import os

import boto3
import meilisearch
import pandas as pd
from botocore.config import Config

from scripts.utils import name_to_key


_project_name = "frataga"
_bucket_name = "archetypes"

def get_image_path(arch: str) -> str:
    arch_dir = os.path.join("images", arch)
    for img in os.listdir(arch_dir):
        if img.endswith(".png"):
            return os.path.join(arch_dir, img)
    raise ValueError(f"Image {arch} not found in images ")


s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_URL"),
    aws_access_key_id=os.environ.get("MINIO_USER"),
    aws_secret_access_key=os.environ.get("MINIO_PASSWORD"),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)


def push_into_db(data_file: str, project_name: str, minio_bucket: str):
    """
    Push the data into a meilisearch database
    """
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    df = pd.read_json(data_file).T
    df["name"] = df.index.to_series()
    df["id"] = df["name"].apply(name_to_key)
    df["project"] = project_name
    df["picture_minio_key"] = f"{project_name}/" + df["id"] + ".png"
    # for arch in df.index:
    #     name = df.loc[arch]["name"]
    #     minio_key = df.loc[arch]["minio_key"]
    #     s3.upload_file(get_image_path(name), minio_bucket, minio_key)
    #     # TODO add palette here too
    df.set_index("id")
    documents = df.to_dict(orient="records")
    index = client.index("archetypes")
    # task = index.add_documents(documents)
    task = index.update_documents(documents)
    index.wait_for_task(task.task_uid)

if __name__ == '__main__':
    push_into_db("data_format.json", _project_name, _bucket_name)