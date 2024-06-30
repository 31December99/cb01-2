# -*- coding: utf-8 -*-
# StreamingCommunity discord server
# @Urlo30 - https://discord.com/invite/8vV68UGRc7
# ------------------------------------------------- #
import re
import string

import requests


def true_link(response: requests):
    [s1, s2] = re.search(r"\}\('(.+)',.+,'(.+)'\.split", response).group(1, 2)
    schema = s1.split(";")[2][5:-1]
    terms = s2.split("|")
    charset = string.digits + string.ascii_letters
    d = dict()

    for i in range(len(terms)):
        try:
            d[charset[i]] = terms[i] or charset[i]
        except IndexError:
            print("Link non disponibile")
            return ''
    s = 'https:'
    for c in schema:
        s += d[c] if c in d else c
    return s
