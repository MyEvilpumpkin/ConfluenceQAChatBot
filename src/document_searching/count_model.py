from sklearn.feature_extraction.text import CountVectorizer as Vectorizer

from .cosine_similarity_model import CosineSimilarityModel


class CountModel(CosineSimilarityModel):
    """
    Count vectorization + Cosine similarity
    """

    def __init__(self):
        """
        Initialize CosineSimilarityModel with the specific CountVectorizer
        """

        super().__init__(Vectorizer(ngram_range=(1, 4)))
