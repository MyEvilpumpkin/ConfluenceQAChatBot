import abc

from src.documents import Document

from .model_result import ModelResult


class Model(abc.ABC):
    """
    Document searching mode base class
    Provides a consistent interface across different model implementations
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def fit(self, documents: list[Document]) -> None:
        pass

    @abc.abstractmethod
    def predict(self, message: str, n_results: int = 1) -> list[ModelResult] | None:
        pass
