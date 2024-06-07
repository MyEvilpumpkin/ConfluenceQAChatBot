from sklearn.feature_extraction.text import TfidfVectorizer as Vectorizer

from .cosine_similarity_model import CosineSimilarityModel


class TfidfModel(CosineSimilarityModel):
    """
    TF-IDF vectorization + Cosine similarity
    """

    def __init__(self):
        """
        Initialize CosineSimilarityModel with the specific TfidfVectorizer
        """

        super().__init__(Vectorizer(ngram_range=(1, 4), sublinear_tf=True, smooth_idf=False))
