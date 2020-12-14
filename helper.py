import re
import const


def convert_float_to_percentage(n):
    return "{}%".format("{0:.3f}".format(float(n) * 100).rstrip('0'))

def get_version():
    with open('Makefile', 'r') as makefile:
        for line in makefile:
            version = re.search(const.REGEX_VERSION, line)
            if version:
                return version.group(2)
