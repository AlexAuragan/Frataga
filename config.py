class Vectorizers:
    #  Ce modèle multilingue est efficace pour les tâches de similarité sémantique en français. Il est léger et offre
    #  de bonnes performances générales.
    pm_minilm = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    # Une version multilingue du modèle paraphrase-mpnet-base-v2, entraînée sur des données parallèles pour plus de 50
    # langues, y compris le français.
    pm_mpnet = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    # Version multilingue distillée du modèle Universal Sentence Encoder, supportant plus de 50 langues. Il est
    # performant pour évaluer la similarité sémantique entre des phrases en français.
    distiluse = "sentence-transformers/distiluse-base-multilingual-cased-v2"

    # Un modèle spécifiquement affiné pour le français, basé sur CamemBERT-base. Il est conçu pour capturer les
    # nuances sémantiques des phrases françaises et est particulièrement adapté aux tâches de similarité
    # sémantique dans cette langue.
    camembert = "dangvantuan/sentence-camembert-base"

class DimensionsReductionMethods:
    umap = "umap"
    pca = "pca"

VECTORIZER = Vectorizers.camembert
NB_DIMENSIONS = 50
DIMENSIONS_REDUCTION_METHOD = DimensionsReductionMethods.pca