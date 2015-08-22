
from __future__ import absolute_import
import re


SN_LANGUAGE_CODE_REGEX = r'-[A-Z]{1,2}'


def sn_is_valid(set_number):
    return (re.match(r'\w+-[A-Z]*\w{3}', set_number) is not None)


def sn_has_language_code(set_number):
    return (re.search(SN_LANGUAGE_CODE_REGEX, set_number) is not None)


def sn_normalize(set_number, with_language_code=True):
    if sn_has_language_code(set_number):
        replace = '-EN'

        if not with_language_code:
            replace = '-'

        normalized_sn = re.sub(SN_LANGUAGE_CODE_REGEX, replace, set_number)
    else:
        replace = '-'

        if with_language_code:
            replace = '-EN'

        normalized_sn = re.sub(r'-', replace, set_number)

    return normalized_sn
