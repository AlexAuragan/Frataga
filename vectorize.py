import umap
from sentence_transformers import SentenceTransformer
from transformers import CamembertModel
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

import config
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
_vectorizer = SentenceTransformer(config.VECTORIZER)

def make_text(data: dict)->str:
    """
    on par du principe que les colones sont 'category', 'description_en', 'tags_fr', 'description_fr', 'color',
       'sub_category', 'values'
    :param data: c'est la donnée d'un personnage
    :return: renvoie le texte qui se fera vectoriser
    """
    output = data["category"] + data["description_fr"] + " tags: " +data["tags_fr"]
    return output


def make_vector(text : str)-> np.array: #array : liste mais plus efficace pour vectoriser
    """
    permet de vectoriser le text
    :param text: la description et le tags du personnage (l'output de la fonction make_text)
    :return: la vectorisation des descriptions
    """
    vector = _vectorizer.encode(text)
    return vector


def init_reduce_dims_model() -> umap.UMAP | PCA:
    if config.DIMENSIONS_REDUCTION_METHOD == config.DimensionsReductionMethods.umap:
        # "rb" comme "read bytes", on lit les fichiers sous format bytes.
        with open(os.path.join("umap_models", config.VECTORIZER.split("/")[-1]+f"_{config.NB_DIMENSIONS}.pkl"), "rb") as f:
            return pickle.load(f) # Return UMAP model
    elif config.DIMENSIONS_REDUCTION_METHOD == config.DimensionsReductionMethods.pca:
        with open(os.path.join("pca_models", config.VECTORIZER.split("/")[-1]+f"_{config.NB_DIMENSIONS}.pkl"), "rb") as f:
            return pickle.load(f) # Return PCA model
    raise ValueError(config.DIMENSIONS_REDUCTION_METHOD)

def reduce_input(vector: np.ndarray, model: umap.UMAP | PCA ) -> np.ndarray:
    return model.transform(np.array([vector]))


def vectorize_input(text:str, model: umap.UMAP | PCA):
    vector_input = make_vector(text)
    reduced_vector = reduce_input(vector_input, model)[0]
    return reduced_vector



def distance(vector_1, vector_2) -> float:
    """
    Calcule la distance entre deux vecteur
    :param vector_1:
    :param vector_2:
    :return: distance
    """

    vector_1 = np.array(vector_1).reshape(1, -1)  # Reformate en 2D gpt
    vector_2 = np.array(vector_2).reshape(1, -1)  # Reformate en 2D gpt
    return 1 - cosine_similarity(vector_1, vector_2)


    #ouvrir data_format.json avec pandas
def arch_finder(text:str,vectors_dict:dict, model: umap.UMAP | PCA):
    input_reduced_vector=vectorize_input(text, model)
    min_key=None
    min_distance=None
    for vector in vectors_dict.keys():
        dist = distance(input_reduced_vector,list(vector))
        if min_distance is None:
            min_distance = dist
            min_key=vector
        elif dist < min_distance:
            min_distance = dist
            min_key=vector
    return vectors_dict[tuple(min_key)]
    # trouver le vecteur associer à reduced_vector
    # regarder où se situe la bonne colonne
    # mettre les vecteurs de la bonne colonne sous forme de dict : key = vecteur value = arch






if __name__ == '__main__':
    model = init_reduce_dims_model()
    df = pd.read_json("data_format.json").T #.T inverse les lignes et les colones
    #print(df.head())
    #print(df.columns)



    vectors_dict = {}
    for arch in df.index:
        value = arch
        key = df.loc[arch][f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS}"]
        vectors_dict[tuple(key)] = value
    while True:
        text=input("Entrer un texte:")
        if text == "exit":
            exit()
        match = arch_finder(text,vectors_dict, model)
        print(f"ton match est {match}")