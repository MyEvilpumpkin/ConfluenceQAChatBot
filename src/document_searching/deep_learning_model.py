import random

import numpy as np
from keras import Sequential, layers, optimizers
from sklearn.feature_extraction.text import CountVectorizer as Vectorizer

from src.documents import Document
from src.preprocessing import process_text

from .model import Model
from .model_result import ModelResult


class DeepLearningModel(Model):
    """
    Document searching model based on deel learning
    """

    def __init__(self):
        """
        Set up internal variables
        """

        self.__documents: list[Document] | None = None
        self.__model: Sequential | None = None
        self.__vectorizer: Vectorizer = Vectorizer(binary=True)
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

        # Generate deep learning model training data
        model_input, model_output = self.__generate_training_data(self.__documents, self.__document_vectors)

        # Create deep learning model
        self.__model = self.__create_model(len(model_input[0]), len(model_output[0]))

        # Train deep learning model
        self.__model.fit(np.array(model_input), np.array(model_output), epochs=200, batch_size=40, verbose=1)

    def predict(self, message: str, n_results: int = 1) -> list[ModelResult] | None:
        """
        Predict documents by using deep learning
        """

        # Process message
        processed_message = process_text(message)

        # Create vector for message
        message_vector = self.__vectorizer.transform([processed_message])

        # Generate deep learning model input
        model_input = message_vector.toarray()

        # Predict deep learning model output
        scores = self.__model.predict(np.array(model_input), verbose=0)[0]

        # Compute top N document indices
        top_n_indices = np.argsort(scores)[-n_results:][::-1]

        # Create model result with soft max score
        top_n_results = [ModelResult(self.__documents[i], scores[i]) for i in top_n_indices]

        return top_n_results

    @staticmethod
    def __generate_training_data(documents: list[Document], document_vectors) -> tuple:
        train_data = []

        for document_index, document in enumerate(documents):
            input_row = document_vectors[document_index].toarray().flatten()
            output_row = np.zeros(len(documents))
            output_row[document_index] = 1

            # train_data.append((input_row, output_row))

            # Augmentation
            words = np.where(input_row == 1)[0]
            words_len = len(words)
            k_min = min(3, words_len)
            k_max = min(7, words_len)
            for _ in range(30):
                k = random.randrange(k_min, k_max)
                local_words = set(random.choices(list(words), k=k))
                local_input_row = np.zeros(len(input_row))
                for word in local_words:
                    local_input_row[word] = 1
                train_data.append((local_input_row, output_row))

        random.shuffle(train_data)

        model_input = [row for row, _ in train_data]
        model_output = [row for _, row in train_data]

        return model_input, model_output

    @staticmethod
    def __create_model(input_size: int, output_size: int) -> Sequential:
        model = Sequential()
        model.add(layers.Dense(128, input_shape=(input_size,), activation='relu'))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(output_size, activation='softmax'))

        sgd = optimizers.SGD(learning_rate=0.01, momentum=0.9)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        return model
