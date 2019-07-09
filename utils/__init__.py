# PrettyPrinter
import pprint
pp = pprint.PrettyPrinter(indent=4, depth=10, width=140)


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


def __open_file_test(fb2book_obj):
    pp.pprint(get_instance_vals(fb2book_obj.description.title_info))
    pp.pprint(get_instance_vals(fb2book_obj.description.document_info))
    pp.pprint(get_instance_vals(fb2book_obj.description.publish_info))
    pp.pprint(get_instance_vals(fb2book_obj.description.custom_info))
    pp.pprint(get_instance_vals(fb2book_obj.body))


def json_to_html(json_data, convert_tags=False):
    TAGS_DICT = {'p': 'p',
                 'title': 'h2',
                 'cite': 'cite',
                 'section': 'div',
                 'a': 'a',
                 'emphasis': 'b',
                 'empty-line': 'div',
                 'image': 'img',
                 'sup': 'sup',
                 'strong': 'strong',
                 'sub': 'sub'}
    text = ''
    for item in json_data:
        text += '<%s>' % TAGS_DICT[item['tag']] if convert_tags else item['tag']
        text += item['text']

        if item['subitems']:
            text += json_to_html(item['subitems'], convert_tags)

        text += item['tail']
        text += '</%s>' % TAGS_DICT[item['tag']] if convert_tags else item['tag']

    return text