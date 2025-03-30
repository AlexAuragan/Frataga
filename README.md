# DnD embeddings - FR

Ce projet est une interface permettant de trouver des personnages / archetypes de type
héroïque-fantaisie parmi une base de données.

## Motivation
Ce projet a été initié par [Aurizon128](https://github.com/Aurizon128) puis aidé par 
[AlexAuragan](https://github.com/AlexAuragan) qui s'occupe également de self-host l'interface 
à https://auragan.duckdns.org/frataga/.

Étant tous les deux français, nous avons décidé d'utiliser cette langue dans notre méthode. 
Les descriptions et embeddings sont donc, pour l'instant calculé en français.

## Prompting

Pour avoir de meilleurs résultats, nous conseillons de faire des phrases complètes vous décrivant 
en termes de traits de caractère ou de vos valeurs, ou celle d'un personnage.

Exemples de prompts:
* `J'aime le travail bien fait`
* `je suis discret et rapide`
* `J'utilise des magies interdites`

Le projet est récent et pour le moment, nous trouvons que le moteur de recherche a encore des lacunes
quand le prompt utilise un langage plus terre-à-terre et sortant de l'univers fantastique.

## Sets d'archetypes:
1. **Frataga** - Le premier set qui a été utilisé comme preuve de concept, regroupant 80 archetypes
différents proposés par ChatGPT
2. À venir

## Méthodologie
1. Nous avons prompté ChatGPT pour obtenir une liste d'archetypes fantastiques.
2. Pour chacun de ces archetypes, nous avons prompté ChatGPT pour obtenir
   * Une description sémantique
   * Une liste de tags
   * Une description physique
3. Nous avons passé les descriptions physiques dans Midjourney avec les options suivantes `--chaos 10 --sref 4266228653 --profile rr1527q`
4. Nous avons utilisé [Camembert](https://huggingface.co/dangvantuan/sentence-camembert-base) pour transformer les descriptions 
et tags en vecteurs, puis utilisé l'algorithme [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis) pour les réduire à 50 dimensions.
5. Pour chaque prompt utilisateur, nous calculons le vecteur associé de la même façon, et nous utilisons la distance cosinus pour trouver 
le vecteur de notre base de données le plus proche.

## Mentions
* Nous nous sommes grandement inspiré de [ce post](https://x.com/JungleSilicon/status/1865835664278790389) par [Jungle Silicon](https://x.com/JungleSilicon)

## Roadmap
* [ ] Rajouter des éléments de contextes sur la page streamlit
* [ ] Ajouter une page pour parcourir tous les archetypes
* [ ] Ajouter d'autres moyens de trouver un archetypes, comme des tests de personnalités
* [ ] Ajouter d'autres sets d'archetypes, comme les classes officielles de DnD