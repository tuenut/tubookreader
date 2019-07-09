import json
from lxml import etree

from backend.parsers import FB2TitleParser, FB2DocumentInfoParser, FB2PublishInfoParser, FB2CustomInfoParser, \
    FB2BodyParser
from utils import json_to_html


# PrettyPrinter
import pprint
pp = pprint.PrettyPrinter(indent=4, depth=10, width=140)


class FB2Description:
    def __init__(self):
        self.title_info = FB2TitleParser()            # required
        self.source_info = FB2TitleParser()
        self.document_info = FB2DocumentInfoParser()  # required
        self.publish_info = FB2PublishInfoParser()
        self.custom_info = FB2CustomInfoParser()

    def configure(self, book_etree, namespace):
        description_element = book_etree.find(etree.QName(namespace, 'description'))

        self.title_info.configure(description_element.find(etree.QName(namespace, 'title-info')), namespace)
        self.document_info.configure(description_element.find(etree.QName(namespace, 'document-info')), namespace)
        self.publish_info.configure(description_element.find(etree.QName(namespace, 'publish-info')), namespace)
        self.custom_info.configure(description_element.find(etree.QName(namespace, 'custom-info')), namespace)


class FB2Body(FB2BodyParser):
    def configure(self, book_etree, namespace):
        super().configure(book_etree.find(etree.QName(namespace, 'body')), namespace)

    def get_sections(self):
        return json.dumps(self.table_of_contents)


class FB2Book:
    # TODO _binary_class = None сделать binary блок из fb2 (картинки, etc)
    def __init__(self, file_path=None):
        self._namespace = None
        self.book_etree = None
        self.description = FB2Description()
        self.body = FB2Body()

        if file_path:
            self.load(file_path)

    def load(self, file_path):
        try:
            self.book_etree = etree.parse(file_path)
        except Exception as e:
            print(e)
            return

        self._namespace = self.book_etree.getroot().nsmap[None]

        self.description.configure(self.book_etree, self._namespace)
        self.body.configure(self.book_etree, self._namespace)


if __name__ == "__main__":
    from locals import TEST_BOOK
    book = FB2Book(file_path=TEST_BOOK)
    data = json.loads(book.body.get_sections())
    # pp.pprint(data)

    with open('test.html', 'w', encoding='utf8') as file:
        file.write(
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
</head>
<body>
""")
        for item in data:
            file.write(json_to_html(item['section']))
        file.write("""</body></html>""")
