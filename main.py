from book import FB2BookClass
from locals import *


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


fb2 = FB2BookClass(TEST_BOOK)

pp.pprint(get_instance_vals(fb2.description.title_info))
pp.pprint(get_instance_vals(fb2.description.document_info))
pp.pprint(get_instance_vals(fb2.description.publish_info))
pp.pprint(get_instance_vals(fb2.description.custom_info))
pp.pprint(get_instance_vals(fb2.body))
