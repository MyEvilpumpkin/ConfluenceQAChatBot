import sys

import streamlit as st
from streamlit.web import cli as stcli

from src.document_searching import TfidfModel
from src.streamlit_app import app
from src.utils.loader import get_model
from src.utils.question_handler import question_handler


if __name__ == '__main__':
    model = get_model(TfidfModel)

    if st.runtime.exists():
        app.start(question_handler(model))
    else:
        sys.argv = ['streamlit', 'run', sys.argv[0]]
        sys.exit(stcli.main())
