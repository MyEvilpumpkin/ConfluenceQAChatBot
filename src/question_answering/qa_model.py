import nltk
from nltk import sent_tokenize

from .pipeline_loader import pipeline

# Load a pre-trained question answering model using Hugging Face's Transformers library
model = pipeline('question-answering', model='IProject-10/xlm-roberta-base-finetuned-squad2')


def find_answer_boundaries(answer_text, context):
    """
    Find the sentences before, within, and after of the answer text within the given context
    """

    nltk.download('punkt', quiet=True)

    sentences = sent_tokenize(context)

    for index, sentence in enumerate(sentences):
        if answer_text in sentence:
            return (
                sentences[index-1] if index > 0 else "",
                sentences[index],
                sentences[index+1] if index < len(sentences) - 1 else ""
            )

    return


def answer(question: str, context: str) -> str:
    """
    Answer a given question based on a provided context
    """

    result = model(question=question, context=context)
    answer_text = result['answer']

    if answer_text in context:
        previous_sentence, sentence, next_sentence = find_answer_boundaries(answer_text, context)

        return f'{previous_sentence}\n\n<b>{sentence}</b>\n\n{next_sentence}'

    return answer_text.capitalize()
