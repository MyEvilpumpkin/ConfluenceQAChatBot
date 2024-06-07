from src.documents import Document


class ModelResult:
    """
    Document searching model result representation
    Attributes:
        document: Document
        score: float
    """

    def __init__(self, document: Document | None = None, score: float = 0.0):
        self.document: Document | None = document
        self.score: float = score
