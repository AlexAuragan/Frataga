from sentence_transformers import SentenceTransformer
import tomllib
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import pandas as pd
import numpy as np
import config
from typing import TYPE_CHECKING, Union
import torch
import random

torch.manual_seed(42)
np.random.seed(42)
random.seed(42)


if TYPE_CHECKING:
    from umap import UMAP
    from sklearn.decomposition import PCA


# Load the vectorizer model based on the config
_vectorizer = SentenceTransformer(config.VECTORIZER)

# Load the field weights from the TOML configuration
_df_config = tomllib.loads(open("fields.toml", "r").read())


def _get_model_filename(model_type: str, collection_name: str) -> str:
    encoder = config.VECTORIZER.split("/")[-1]
    return os.path.join(f"{model_type}_models", f"{encoder}_{config.NB_DIMENSIONS[collection_name]}-{collection_name}.pkl")

def _reduce_dims_umap(embeddings: np.ndarray, collection_name: str, save: bool = True) -> list[np.ndarray]:
    from umap import UMAP
    umap_model = UMAP(n_components=config.NB_DIMENSIONS[collection_name], random_state=42)
    reduced_embeddings = umap_model.fit_transform(embeddings)
    if save:
        with open(_get_model_filename("umap", collection_name), "wb") as f:
            pickle.dump(umap_model, f)
    return reduced_embeddings.tolist()


def _reduce_dims_pca(embeddings: np.ndarray, collection_name: str, save: bool = True) -> list[np.ndarray]:
    from sklearn.decomposition import PCA
    pca_model = PCA(n_components=config.NB_DIMENSIONS[collection_name])
    reduced_embeddings = pca_model.fit_transform(embeddings)
    if save:
        with open(_get_model_filename("pca", collection_name), "wb") as f:
            pickle.dump(pca_model, f)
    return reduced_embeddings.tolist()

def make_text(data: dict) -> str:
    """
    Construct a weighted string from a data dictionary using field weights from fields.toml.
    Used to improve quality of embeddings by duplicating important features.

    :param data: Data dictionary representing one archetype.
    :return: Weighted string representation ready for vectorization.
    """
    output = ""
    for field, weight in _df_config.items():
        output += data[field] * weight + " "
    return output


def make_vector(text: str) -> np.ndarray:
    """
    Generate an embedding vector from the given text using the SentenceTransformer model.

    :param text: Weighted string input (output of `make_text`).
    :return: Vectorized representation as a NumPy array.
    """
    vector_input: np.ndarray = _vectorizer.encode(text, convert_to_numpy=True)
    return vector_input


def init_reduce_dims_model(collection_name: str) -> Union["UMAP", "PCA", None]:
    """
    Load the appropriate dimension reduction model from disk, based on config.

    :return: Loaded UMAP or PCA model.
    """
    method = config.DIMENSIONS_REDUCTION_METHOD
    if method == config.DimensionsReductionMethods.umap:
        with open(_get_model_filename("umap", collection_name), "rb") as f:
            return pickle.load(f)
    elif method == config.DimensionsReductionMethods.pca:
        with open(_get_model_filename("pca", collection_name), "rb") as f:
            return pickle.load(f)
    elif method == config.DimensionsReductionMethods.none:
        return None
    raise ValueError(method)


def reduce_input(vector: np.ndarray, model: Union["UMAP", "PCA", None]) -> np.ndarray:
    """
    Reduce a single high-dimensional vector using the given UMAP/PCA model.

    :param vector: The high-dimensional vector to reduce.
    :param model: The dimensionality reduction model.
    :return: The reduced vector in NumPy array format.
    """
    if model is None:
        reduced = vector
    else:
        reduced = model.transform(np.array([vector]))[0]
    reduced /= np.linalg.norm(reduced)
    return reduced


def vectorize_input(text: str, model: Union["UMAP", "PCA", None]) -> np.ndarray:
    """
    Convert input text to its reduced vector representation.

    :param text: User input or free text to be compared.
    :param model: Dimension reduction model (UMAP or PCA).
    :return: A single reduced vector.
    """

    vector_input = make_vector(text)
    reduced_vector = reduce_input(vector_input, model)
    return reduced_vector


def distance(vec_a: list[float] | np.ndarray, vec_b: list[float] | np.ndarray) -> float:
    """
    Compute cosine distance (1 - cosine similarity) between two vectors.

    :param vec_a: First vector.
    :param vec_b: Second vector.
    :return: Cosine distance as float.
    """

    vec_a /= np.linalg.norm(vec_a)
    vec_b /= np.linalg.norm(vec_b)
    v1 = np.array(vec_a).reshape(1, -1)
    v2 = np.array(vec_b).reshape(1, -1)
    return 1 - cosine_similarity(v1, v2)


def arch_finder(text: str, vectors_dict: dict[tuple[float], str], model: Union["UMAP", "PCA", None]) -> str:
    """
    Identify the closest archetype vector from a dictionary using cosine distance.

    :param text: User input to match against stored archetypes.
    :param vectors_dict: Dictionary mapping reduced vectors to archetypes.
    :param model: The dimensionality reduction model used for consistency.
    :return: Archetype with the smallest distance.
    """
    input_reduced_vector = vectorize_input(text, model)
    min_key = None
    min_distance = None

    for vector in vectors_dict:
        dist = distance(input_reduced_vector, list(vector))
        if min_distance is None or dist < min_distance:
            min_distance = dist
            min_key = vector

    return vectors_dict[tuple(min_key)]
