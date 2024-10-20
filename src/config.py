import os
from configparser import ConfigParser

BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))

def config(filename=BASE_PATH + "/database.ini", section="postgresql") -> dict:
    """Config for database"""

    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db