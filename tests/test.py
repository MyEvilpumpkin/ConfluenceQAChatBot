from src.utils.loader import get_model
from src.document_searching import *

questions = [
    # Set up test questions
]


if __name__ == '__main__':
    model = get_model(TfidfModel)

    for index, question in enumerate(questions, start=1):
        result = model.predict(question)[0]
        document = result.document
        score = result.score
        print(f'{index} - {document.title} - {score} - {document.link}')
