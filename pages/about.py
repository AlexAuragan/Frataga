import streamlit as st

from front.sidebar import sidebar


def about():
    st.title("À propos")
    st.text("Ce projet a été initié par Aurizon128 dans le cadre du lycée et a été codirigé par AlexAuragan.")

    st.header("Pourquoi l'univers de DnD ?")
    st.text("Le but original n'était pas forcément de se baser sur l'univers de DnD, mais cela nous semblait un choix "
            "simple pour commencer. Inspiré par le travail de Jungle Silicon sur X, nous avons pensé à faire le même "
            "travail sur de archetypes de roman, divinité antiques, autres univers connus, etc.\n"
            "Nous explorons actuellement la possibilité de rajouter de nouvelles 'collections'.")

    st.header("Utilisation de Midjourney")
    st.text("Nous avons décider d'utiliser Midjourney pour la génération d'images.\n"
            "Si nous sommes contre contre le vol du travail d'artistes, nous somme obligé que ce projet n'aurait jamais été possible sans l'utilisation d'IA pour la génération de graphismes."
            "Les illustration sont essentielles à l'attrait du site, et des bonhommes batons faits sur paint n'auraient pas eu le même impact. Notre but premier est de rendre l'expérience la plus"
            " fun et agréable possible, et nous avons calculer qu'utiliser une IA générative était la façon la plus efficace d'y arriver.\n"
            "Si un artiste se porte volontaire pour refaire à la main les 200+ images du sites, nous les accepterions "
            "volontier contre 50% du revenu du site (Actuellement 0€/mois).\n"
            "Vous serez alors payé à la même hauteur que les deux auteurs du projet réunis et qui y ont déjà investis plusieurs dizaines d'heures."
            )
    st.text("Les images utilisées dans la première collection ont été générée avec comme suffixe "
            "`--chaos 10 --sref 4266228653 --profile rr1527q`. Les prompts entiers ont été générés par ChatGPT.\n"
            "Étant donné que nous n'avons eu que très peu d'impact quant-à la création de ses images, nous ne pouvons"
            " pas nous en approprier la propriété intellectuelle. Elles sont donc libre de droits pour tous et tout"
            " usages, dans la limite des lois applicables. \n"
            "Les images de la collection Greek Gods ont été générées avec comme suffixe `--chaos 15 --weird 200` et cette fois en utilisant diverses images comme référence.")

    st.header("Langue")
    st.text("Étant donné le cadre de notre projet, nous avons fais le choix d'utiliser un vectorizer français "
            "(Camembert), donc l'application est faite pour être promptée en français. Par conséquent, il est logique"
            " que le reste du site soit également en français.\n"
            "Nous ne sommes pas fermé à l'idée de traduire l'application et d'en faire une version anglaise, mais il"
            " faut que je besoin s'en fasse ressentir.")
if __name__ == '__main__':
    sidebar()
    about()
