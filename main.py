import config
import format
from vectorize import init_reduce_dims_model, arch_finder
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    for n in range(2, 200):
        config.NB_DIMENSIONS = n
        format.vectorize_data(input_path="data_format.json")
        model = init_reduce_dims_model()
        df = pd.read_json("data_format.json").T #.T inverse les lignes et les colones
        vectors_dict = {}
        for arch in df.index:
            value = arch
            key = df.loc[arch][f"vector:{config.VECTORIZER}:reduced:{config.NB_DIMENSIONS}"]
            vectors_dict[tuple(key)] = value
        del df
        score = 0
        for arch in list(vectors_dict.values()):
            match = arch_finder(arch,vectors_dict, model)
            if match == arch:
                score += 1
        print(f"Quand {n=} on a {score} match qui correspondent à leur archetype")
