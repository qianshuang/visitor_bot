# -*- coding: utf-8 -*-

from common import *
import string
import marisa_trie
import re

# 构建原始标准问映射
intents = read_file("data/intents.txt")
intents_lower_dict = {intent.lower(): intent for intent in intents}

# 构建Trie树
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


query_ = "Convert "
print(smart_hint(query_))
print(query_)
