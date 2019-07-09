from lxml import etree
import json


class FB2ParserMixin:
    _attributes = dict()

    def __init__(self):
        self.__namespace = None

    @staticmethod
    def parse_element(element):
        children = element.getchildren()
        if not children:
            return element if element.attrib else element.text.strip()

        return children if len(children) > 1 else children[0]

    def _attributes_control(self, attribute_name):
        if attribute_name in self._attributes:
            return True
        else:
            return False

    def configure(self, element, namespace):
        if element is None:
            return

        for el in element.getchildren():
            parsed_data = self.parse_element(el)
            clear_tag_name = el.tag.replace('{%s}' % namespace, '').replace('-', '_')

            if not self._attributes_control(clear_tag_name):
                continue

            try:
                if isinstance(parsed_data, (list, tuple, set)):
                    getattr(self, clear_tag_name, ).extend(parsed_data)
                else:
                    getattr(self, clear_tag_name, ).append(parsed_data)
            except AttributeError:
                setattr(self, clear_tag_name, parsed_data)
            except TypeError:
                attribute_value = getattr(self, clear_tag_name, )
                setattr(self, clear_tag_name, [attribute_value, parsed_data])


class FB2TitleParser(FB2ParserMixin):
    _attributes = dict(
        genre={'required': True, 'only_one': False},
        author={'required': True, 'only_one': False},
        book_title={'required': True, 'only_one': True},
        annotation={'required': False, 'only_one': True},
        keywords={'required': False, 'only_one': True},
        date={'required': False, 'only_one': True},
        coverpage={'required': False, 'only_one': True},
        lang={'required': True, 'only_one': True},
        src_lang={'required': False, 'only_one': True},
        translator={'required': False, 'only_one': False},
        sequence={'required': False, 'only_one': False},
    )
    genre = None
    author = None
    book_title = None
    annotation = None
    keywords = None
    date = None
    coverpage = None
    lang = None
    src_lang = None
    translator = None
    sequence = None


class FB2DocumentInfoParser(FB2ParserMixin):
    _attributes = dict(
        author={'required': True, 'only_one': False},
        program_used={'required': False, 'only_one': True},
        date={'required': True, 'only_one': True},
        src_url={'required': False, 'only_one': False},
        src_ocr={'required': False, 'only_one': True},
        fb2_id={'required': True, 'only_one': True},
        version={'required': True, 'only_one': True},
        history={'required': False, 'only_one': True},
        publisher={'required': False, 'only_one': False},
    )
    author = None
    program_used = None
    date = None
    src_url = None
    src_ocr = None
    fb2_id = None
    version = None
    history = None
    publisher = None


class FB2PublishInfoParser(FB2ParserMixin):
    _attributes = dict(
        book_name={'required': False, 'only_one': True},
        publisher={'required': False, 'only_one': True},
        city={'required': False, 'only_one': True},
        year={'required': False, 'only_one': True},
        isbn={'required': False, 'only_one': True},
        sequence={'required': False, 'only_one': False},
    )
    book_name = None
    publisher = None
    city = None
    year = None
    isbn = None
    sequence = None


class FB2CustomInfoParser(FB2ParserMixin):
    def _attributes_control(self, attribute_name):
        return True


class FB2BodyParser(FB2ParserMixin):
    _attributes = dict(
        image={'required': False, 'only_one': True},
        title={'required': False, 'only_one': True},
        epigraph={'required': False, 'only_one': False},
        section={'required': True, 'only_one': False},
    )
    image = None
    title = None
    epigraph = None
    table_of_contents = list()

    def __parse_title(self, title_element):
        result = list()

        if title_element.text.strip():
            result.append(title_element.text.strip())

        for el in title_element.getchildren():
            if not el.getchildren():
                result.append(el.text.strip())
            else:
                result.extend(self.__parse_title(el))
        if title_element.tail.strip():
            result.append(title_element.tail.strip())

        return result

    def parse_section(self, section_element=None):
        section_element = self.table_of_contents[0]['section'] if section_element is None else section_element
        result = list()

        section_dict = dict(
            tag=section_element.tag.replace('{%s}' % self.__namespace, ''),
            text=section_element.text.strip() if section_element.text else '',
            tail=section_element.tail.strip() if section_element.tail else '',
            subitems=list()
        )

        for el in section_element.getchildren():
            if not el.getchildren():
                section_dict['subitems'].append(dict(
                    tag=el.tag.replace('{%s}' % self.__namespace, ''),
                    text=el.text.strip() if el.text else '',
                    tail=el.tail.strip() if el.tail else '',
                    subitems=list()
                ))
            else:
                section_dict['subitems'].extend(self.parse_section(el))

        result.append(section_dict)

        return result

    def configure(self, body, namespace):
        self.__namespace = namespace

        if body is None:
            return

        self.image = body.find(etree.QName(namespace, 'image'))
        self.title = body.find(etree.QName(namespace, 'title'))
        self.epigraph = body.find(etree.QName(namespace, 'epigraph'))

        for section in body.findall(etree.QName(namespace, 'section')):
            title = section.find(etree.QName(namespace, 'title'))
            if section.find(etree.QName(namespace, 'title')) is not None:
                self.table_of_contents.append(
                    dict(
                        title=' '.join(self.__parse_title(title)).strip(),
                        section=self.parse_section(section)
                    )
                )
