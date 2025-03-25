import pickle #sauvegarde
import os #sauvegarde
import pandas as pd #pour avoir des Dataframe
import numpy as np #librairie de mathématiques
import umap #outil qui réduit les dimensions
from sklearn.decomposition import PCA # Autre outil pour réduire les dimensions
from sklearn.manifold import TSNE
from tqdm import tqdm

import config
from vectorize import make_text, make_vector


def vectorize_data(input_path : str)-> None:
    """
    permet de stocker les vectorisations
    :param input_path: le chemin vers le json
    :return: None
    """
    df : pd.DataFrame = pd.read_json(input_path).T
    df["vector:" + config.VECTORIZER] = None # Gpt
    for arch in df.index:
        data = df.loc[arch]
        vector = make_vector(make_text(data=data))
        df.at[arch, "vector:"+config.VECTORIZER] = vector
    vectors = reduce_dims(np.vstack(df["vector:" + config.VECTORIZER].to_numpy()), save = True)
    df[f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS}"]=vectors
    df.T.to_json(input_path, indent=4, force_ascii=False)


def reduce_dims(embeddings: np.ndarray, save: bool = True) -> list[np.ndarray]:
    """
    Choisir la bonne méthode pour réduire les dimensions
    :param embeddings:
    :param save:
    :return:
    """
    if config.DIMENSIONS_REDUCTION_METHOD == config.DimensionsReductionMethods.umap:
        return reduce_dims_umap(embeddings, save)
    elif config.DIMENSIONS_REDUCTION_METHOD == config.DimensionsReductionMethods.pca:
        return reduce_dims_pca(embeddings, save)
    raise ValueError(f"Unknown dimensions reduction method", config.DIMENSIONS_REDUCTION_METHOD)


def reduce_dims_umap(embeddings: np.ndarray, save: bool = True) -> list[np.ndarray]:
    """
    Créer un modèle UMAP qui sert à diminuer les dimensions des vecteurs.
    Le modèle est enregistré pour pouvoir être utilisé sur les requêtes des utilisateurs.
    :param embeddings: Vecteurs de hautes dimensions
    :param save: Si oui ou non on sauvegarde le modèle
    :return: Vecteurs de faibles dimensions, le nombre est spécifié par config.NB_DIMENSIONS
    """
    umap_model = umap.UMAP(n_components=config.NB_DIMENSIONS)

    reduced_embeddings = umap_model.fit_transform(embeddings.tolist())
    if save:
        encoder = config.VECTORIZER.split("/")[-1]
        with open(os.path.join("umap_models", encoder +f"_{config.NB_DIMENSIONS}" + ".pkl"), "wb") as f:
            pickle.dump(umap_model, f)
    return reduced_embeddings.tolist()


def reduce_dims_pca(embeddings: np.ndarray, save: bool = True) -> list[np.ndarray]:
    """
    Créer un modèle PCA qui sert à diminuer les dimensions des vecteurs.
    Le modèle est enregistré pour pouvoir être utilisé sur les requêtes des utilisateurs.
    :param embeddings: Vecteurs de hautes dimensions
    :param save: Si oui ou non on sauvegarde le modèle
    :return: Vecteurs de faibles dimensions, le nombre est spécifié par config.NB_DIMENSIONS
    """
    pca_model = PCA(n_components=config.NB_DIMENSIONS)

    reduced_embeddings = pca_model.fit_transform(embeddings.tolist())
    if save:
        encoder = config.VECTORIZER.split("/")[-1]
        with open(os.path.join("pca_models", encoder +f"_{config.NB_DIMENSIONS}" + ".pkl"), "wb") as f:
            pickle.dump(pca_model, f)
    return reduced_embeddings.tolist()


def format_xlsx(input_path:str,output_path:str) -> None:
    """
    la fonction crée un un fichier nommer dataformat avec toutes les informations du xlsx formaté
    :param input_path: le fichier xlsx
    :param output_path: le chemin vers le fichier de sortie
    :return: None
    """
    df : pd.DataFrame = pd.read_excel(input_path)
    df["name"]=df["name"].apply(lambda x: x.strip()) #retire les espaces
    df = df.set_index("name")
    df = df.drop(columns=["Tags","Lien image"])
    for arch in df.index :

        #Format des catégories
        data = df.loc[arch]
        category = data["category"]
        c1,c2=category.split("/")
        c1=c1.strip().lower()
        c2=c2.strip().lower()
        df.at[arch, "category"] = c1
        df.at[arch, "sub_category"] = c2

        #Format des descriptions
        data = df.loc[arch]
        description_fr = data["description_fr"]
        parts = description_fr.split(":")
        name,desc,values=parts

        desc = desc.removesuffix("Valeurs ")
        df.at[arch, "description_fr"] = desc
        df.at[arch, "values"] = values
    df.T.to_json(output_path, indent=4,force_ascii=False)


if __name__ == '__main__':
    # format_xlsx(input_path="archetypes.xlsx", output_path="data_format.json")
    vectorize_data(input_path="data_format.json")