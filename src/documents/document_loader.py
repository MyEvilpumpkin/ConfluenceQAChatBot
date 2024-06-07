import os

from .document import Document
from .document_parser import parse_html_document


def collect_document_file_paths(document_dirs: list[str]) -> list[str]:
    """
    Iterate over all document directories and collect all document file paths
    """

    document_file_paths = list()

    for document_dir in document_dirs:
        for root, _, files in os.walk(document_dir):
            for file_name in files:
                if file_name.endswith('.html'):
                    file_path = os.path.join(root, file_name)
                    document_file_paths.append(file_path)

    return document_file_paths


def load_documents(document_dirs: list[str]) -> list[Document]:
    """
    Collect and parse all documents
    """

    document_file_paths = collect_document_file_paths(document_dirs)

    documents = list()

    for document_file_path in document_file_paths:
        document = parse_html_document(document_file_path)

        if document is not None:
            documents.append(document)

    return documents
