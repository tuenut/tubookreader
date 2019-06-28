import sys

from backend.book import FB2Book
from frontend import start_gui

# PrettyPrinter
import pprint
pp = pprint.PrettyPrinter(indent=4, depth=10, width=140)

from utils import get_instance_vals


def __open_file_test():
    try:
        fb2 = FB2Book(sys.argv[1])
    except:
        raise

    pp.pprint(get_instance_vals(fb2.description.title_info))
    pp.pprint(get_instance_vals(fb2.description.document_info))
    pp.pprint(get_instance_vals(fb2.description.publish_info))
    pp.pprint(get_instance_vals(fb2.description.custom_info))
    pp.pprint(get_instance_vals(fb2.body))


if __name__ == "__main__":
    start_gui()