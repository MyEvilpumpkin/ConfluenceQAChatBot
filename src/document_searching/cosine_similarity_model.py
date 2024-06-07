import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.documents import Document
from src.preprocessing import process_text

from .model import Model
from .model_result import ModelResult


class CosineSimilarityModel(Model):
    """
    Document searching model based on cosine similarity
    """

    def __init__(self, vectorizer: CountVectorizer):
        """
        Initialize the model with a given vectorizer instance and set up internal variables
        """

        self.__documents: list[Document] | None = None
        self.__vectorizer: CountVectorizer = vectorizer
        self.__document_vectors = None

    def fit(self, documents: list[Document]) -> None:
        """
        Train the model on a list of documents
        """

        # Save documents in model
        self.__documents = documents

        # Process each document content
        processed_documents = [process_text(document.content) for document in self.__documents]

        # Create vector for each documents
        self.__document_vectors = self.__vectorizer.fit_transform(processed_documents)

    def predict(self, message: str, n_results: int = 1) -> list[ModelResult] | None:
        """
        Predict documents by using cosine similarity
        """

        # Process message
        processed_message = process_text(message)

        # Create vector for message
        message_vector = self.__vectorizer.transform([processed_message])

        # Compute the cosine similarity between message vector and the document vectors
        scores = cosine_similarity(message_vector, self.__document_vectors).flatten()

        # Compute top N document indices
        top_n_indices = np.argsort(scores)[-n_results:][::-1]

        # Create model result with cosine similarity score
        top_n_results = [ModelResult(self.__documents[i], scores[i]) for i in top_n_indices]

        return top_n_results
