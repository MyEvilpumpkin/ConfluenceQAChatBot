import os

import joblib

from src.documents import Document, load_documents
from src.document_searching import Model

from .config import document_dirs, documents_cache_file, model_cache_file


def get_documents(use_cache: bool = True) -> list[Document]:
    """
    Load documents from cache or raw data
    """

    # Check if documents cache exists
    documents_cache_exists = os.path.exists(documents_cache_file)

    if use_cache and documents_cache_exists:
        # Load from cache
        documents = joblib.load(documents_cache_file)

        return documents

    # Load from raw data
    documents = load_documents(document_dirs)

    # Save to cache
    joblib.dump(documents, documents_cache_file)

    return documents


def get_model(model_type: type, use_cache: bool = True) -> Model:
    """
    Load model from cache or create and fit new model with given type
    """

    # Check if model cache exists
    model_cache_exists = os.path.exists(model_cache_file)

    if use_cache and model_cache_exists:
        # Load from cache
        model = joblib.load(model_cache_file)

        # Check model type
        if isinstance(model, model_type) and isinstance(model, Model):
            return model

    # Load documents
    documents = get_documents()

    # Create and fit new model
    model = model_type()
    model.fit(documents)

    # Save to cache
    joblib.dump(model, model_cache_file)

    return model
