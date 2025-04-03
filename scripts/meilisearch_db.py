import os
import pandas as pd
import meilisearch

from scripts.utils import name_to_key

_project_name = "frataga"
def push_into_meilisearch(data_file: str, project_name: str):
    """
    Push the data into a meilisearch database
    """
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    df = pd.read_json(data_file).T
    df["name"] = df.index.to_series()
    df["id"] = df["name"].apply(name_to_key)
    df["project"] = project_name
    df["minio_key"] = f"{project_name}/" + df["id"] + ".png"

    df.set_index("id")
    documents = df.to_dict(orient="records")
    index = client.index("archetypes")
    # task = index.update_documents(documents)
    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

def get_meilisearch(project_name):
    client = meilisearch.Client(os.environ.get("MEILISEARCH_URL"), os.environ.get("MEILISEARCH_PASSWORD"))
    index = client.index("archetypes")
    all_docs = []
    offset = 0
    limit = 1000

    while True:
        response = index.get_documents({"limit": limit, "offset": offset})
        all_docs.extend(response.results)

        if len(response.results) < limit:
            break  # no more pages
        offset += limit
    return all_docs

if __name__ == '__main__':
    # push_into_meilisearch("data_format.json", _project_name)
    out = get_meilisearch(_project_name)