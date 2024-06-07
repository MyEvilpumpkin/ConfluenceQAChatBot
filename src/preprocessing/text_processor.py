import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy3


def process_text(text: str, remove_stopwords: bool = True, lemmatize: bool = True,
                 min_token_len: int = 2, only_unique_tokens: bool = False, order_tokens: bool = False,
                 as_list: bool = False) -> str | list[str] | None:
    """
    Tokenize and remove stopwords and lemmatize text
    """

    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

    tokens = word_tokenize(text.lower(), language='russian')
    tokens = [token for token in tokens if token.isalpha()]

    if remove_stopwords:
        stop_words = set(stopwords.words('russian'))
        tokens = [token for token in tokens if token not in stop_words]

    if lemmatize:
        morph = pymorphy3.MorphAnalyzer()
        tokens = [morph.parse(token)[0].normal_form for token in tokens]

    if min_token_len > 1:
        tokens = [token for token in tokens if len(token) >= min_token_len]

    if only_unique_tokens:
        tokens = list(set(tokens))

    if order_tokens:
        tokens = sorted(tokens)

    if as_list:
        return tokens

    return ' '.join(tokens)
