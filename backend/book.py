from lxml import etree


class FB2ParserMixin:
    _namespace = None
    _attributes = dict()

    def __init__(self, namespace):
        self._namespace = namespace

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

    def configure(self, element):
        if element is None:
            return

        for el in element.getchildren():
            parsed_data = self.parse_element(el)
            clear_tag_name = el.tag.replace('{%s}' % self._namespace, '').replace('-', '_')


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


class FB2Title(FB2ParserMixin):
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


class FB2DocumentInfo(FB2ParserMixin):
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


class FB2PublishInfo(FB2ParserMixin):
    _attributes = dict(
        book_name={'required': False, 'only_one': True},
        publisher={'required': False, 'only_one': True},
        city={'required': False, 'only_one': True},
        year={'required': False, 'only_one': True},
        isbn={'required': False, 'only_one': True},
        sequence={'required': False, 'only_one': False},
    )


class FB2CustomInfo(FB2ParserMixin):
    def _attributes_control(self, attribute_name):
        return True


class FB2Description:
    _title_info_class = FB2Title  # required
    _source_info_class = FB2Title
    _document_info_class = FB2DocumentInfo  # required
    _publish_info_class = FB2PublishInfo
    _custom_info_class = FB2CustomInfo

    def __init__(self, namespace):
        self._namespace = namespace

    def configure(self, element):
        self.title_info = self._title_info_class(self._namespace)
        self.document_info = self._document_info_class(self._namespace)
        self.publish_info = self._publish_info_class(self._namespace)
        self.custom_info = self._custom_info_class(self._namespace)

        self.title_info.configure(element.find(etree.QName(self._namespace, 'title-info')))
        self.document_info.configure(element.find(etree.QName(self._namespace, 'document-info')))
        self.publish_info.configure(element.find(etree.QName(self._namespace, 'publish-info')))
        self.custom_info.configure(element.find(etree.QName(self._namespace, 'custom-info')))


class FB2Body(FB2ParserMixin):
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

    def element_to_string(self, element):
        result = list()
        if element.text.strip():
            result.append(element.text.strip())

        for el in element.getchildren():
            if not el.getchildren():
                result.append(el.text.strip())
            else:
                result.extend(self.element_to_string(el))
        if element.tail.strip():
            result.append(element.tail.strip())

        return result

    def configure(self, body):
        if body is None:
            return

        self.image = body.find(etree.QName(self._namespace, 'image'))
        self.title = body.find(etree.QName(self._namespace, 'title'))
        self.epigraph = body.find(etree.QName(self._namespace, 'epigraph'))

        for section in body.findall(etree.QName(self._namespace, 'section')):
            title = section.find(etree.QName(self._namespace, 'title'))
            if section.find(etree.QName(self._namespace, 'title')) is not None:
                self.table_of_contents.append((' '.join(self.element_to_string(title)).strip(), section))


class FB2Book:
    _description_class = FB2Description
    _body_class = FB2Body
    _binary_class = None

    def __init__(self, file_name):
        self.book_etree = etree.parse(file_name)
        self._namespace = self.book_etree.getroot().nsmap[None]

        self.description = self._description_class(self._namespace)
        self.body = self._body_class(self._namespace)

        self.description.configure(self.book_etree.find(etree.QName(self._namespace, 'description')))
        self.body.configure(self.book_etree.find(etree.QName(self._namespace, 'body')))
