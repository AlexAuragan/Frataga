import pandas as pd

def format_xlsx(input_path:str,output_path:str) -> None:
    df : pd.DataFrame = pd.read_excel(input_path)
    df["name"]=df["name"].apply(lambda x: x.strip()) #retire les espaces
    df = df.set_index("name")
    df = df.drop(columns=["Tags","Lien image"])
    df = df.drop(index=["Squelette du Gardien"])
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
    format_xlsx(input_path="archetypes.xlsx", output_path="data_format.json")
