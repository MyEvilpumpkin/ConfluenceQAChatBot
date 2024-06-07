from typing import Callable

import streamlit as st


def start(text_message_handler: Callable[[str, int], str]) -> None:
    st.title('Документация')
    text = st.text_area(label='Вопрос', placeholder='Введите вопрос...')
    n_results = st.number_input(label='Количество документов в ответе', min_value=1, value='min', step=1)
    if text != '':
        response = text_message_handler(text, n_results)
        st.write('Ответ:')
        st.markdown(response, unsafe_allow_html=True)
    else:
        st.write('Для получения ответа необходимо ввести вопрос')
