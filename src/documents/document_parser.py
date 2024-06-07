from bs4 import BeautifulSoup

from .document import Document


def parse_html_document(file_path: str) -> Document | None:
    """
    Parse HTML document
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()

        soup = BeautifulSoup(html, 'html.parser')

        title_element = soup.title
        title = title_element.string.strip() if title_element else None

        link_element = soup.find('link', rel='canonical')  # rel='shortlink' for short links
        link = link_element.get('href', None) if link_element else None

        content_element = soup.select_one('#main-content')
        content = content_element.get_text(' ', strip=True) if content_element else None

        if content is None or len(content) == 0:
            return None

        document = Document()
        document.title = title
        document.link = link
        document.content = content
        document.file_path = file_path

        return document
