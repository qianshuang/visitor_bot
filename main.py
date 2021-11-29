# -*- coding: utf-8 -*-

from common import *
import string
import marisa_trie
import re

intents = read_file("data/intents.txt")
intents_lower_dict = {intent.lower(): intent for intent in intents}

trie = marisa_trie.Trie(list(intents_lower_dict.keys()))


def smart_hint(query):
    # 1. 转小写
    query = query.lower()

    # 2. 去标点
    for c in string.punctuation:
        query = query.replace(c, "")

    # 3. 合并空格
    query = re.sub(r'\s+', ' ', query)

    # 4. 前缀匹配
    result = trie.keys(query)

    # 5. 还原原文本
    return [intents_lower_dict[res] for res in result]


print(smart_hint("What "))
