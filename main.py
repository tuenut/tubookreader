# PrettyPrinter
import pprint
pp = pprint.PrettyPrinter(indent=4, depth=10, )

from book import FB2BookClass
from locals import *


def get_instance_vals(instance):
    vals = dict()
    for key in dir(instance):
        if not key.startswith('_') and not callable(getattr(instance, key)):
            try:
                if len(getattr(instance, key)) > 0:
                    vals.update({key: getattr(instance, key)})
            except TypeError:
                if getattr(instance, key):
                    vals.update({key: getattr(instance, key)})
    return vals


fb2 = FB2BookClass(TEST_BOOK)

pp.pprint(get_instance_vals(fb2.description.title_info))
pp.pprint(get_instance_vals(fb2.description.document_info))
pp.pprint(get_instance_vals(fb2.description.publish_info))
pp.pprint(get_instance_vals(fb2.description.custom_info))
pp.pprint(get_instance_vals(fb2.body))



## TODO для парсинга секций боди
def element_to_string(element):
    result = list()
    result.append(element.text.strip())

    for el in element.getchildren():
        if not el.getchildren():
            result.append(el.text.strip())
        else:
            result.extend(element_to_string(el))
    result.append(element.tail.strip())

    return result


table_of_contents = list()

for section in body.findall(etree.QName(namespace, 'section')):
    title = section.find(etree.QName(namespace, 'title'))
    if section.find(etree.QName(namespace, 'title')):
        table_of_contents.append((' '.join(element_to_string(title)).strip(), section))
