from typing import Callable

from src.document_searching import Model
from src.documents import Document
from src.question_answering import answer as answer_question


def link_clickable(link: str) -> bool:
    """
    Check if a given URL string contains a clickable link component
    """

    return '.' in link.split('//')[-1].split('/')[0]


def generate_formatted_document_info(document: Document) -> str:
    """
    Generate a formatted document info string
    """

    # Format the document title for display
    title = f'<pre>{document.title}</pre>'

    # Determine how to format the link based on whether it's clickable and exists
    link = f'<a href="{document.link}">{document.link}</a>' \
        if link_clickable(document.link) else f'<pre>{document.link}</pre>' \
        if document.link else 'Ссылка не найдена'

    # Constructs document info including document name and link
    document_info = f'Наименование: {title}\nСсылка: {link}'

    return document_info


def question_handler(model: Model) -> Callable[[str, int], str]:
    """
    Configure question handler function
    """

    def handle_question(question: str, n_results: int = 1) -> str:
        if n_results == 1:
            # Predicts a single result for the given question
            result = model.predict(question)[0]

            # Get document from result
            document = result.document

            # Generate formatted document info
            document_info = generate_formatted_document_info(document)

            # Generate the answer to the question using the document content
            answer = answer_question(question, document.content)

            # Constructs the full response message
            response = f'{answer}\n\n{document_info}'

            return response
        else:
            # Predicts multiple results for the given question
            results = model.predict(question, n_results=n_results)

            # Initializes an empty string to accumulate the response
            response = ''

            # Iterates over each predicted result to format and append its details to the response
            for index, result in enumerate(results, start=1):
                # Get document from result
                document = result.document

                # Generate formatted document info
                document_info = generate_formatted_document_info(document)

                # Generate document header
                header = f'<b>Документ {index}</b>'

                # Constructs the full response message
                response += f'{header}\n{document_info}\n\n'

            return response

    return handle_question
