# -*- coding: utf-8 -*-

import string
import pandas as pd

from config import *


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

    # 5. 纠错
    if len(result) == 0:
        query = query.strip()
        pres = query.split(" ")[:-1]
        last = query.split(" ")[-1]
        pre_corr_query = " ".join([correction(w) for w in pres])
        result = trie.keys(pre_corr_query + " " + last)
        if len(result) == 0:
            corr_query = pre_corr_query + " " + correction(last)
            result = trie.keys(corr_query)

    # 6. 还原原文本
    return [intents_lower_dict[res] for res in result]


def rank(trie_res):
    frequency_ = []
    recents_ = []
    for item in trie_res:
        if item in frequency:
            frequency_.append(frequency[item])
        else:
            frequency_.append(0)

        if item in recents:
            recents_.append(len(recents) - recents.index(item))
        else:
            recents_.append(0)
    df = pd.DataFrame({"trie_res": trie_res, "frequency": frequency_, "recents": recents_})
    df.sort_values(by=["frequency", "recents"], ascending=False, inplace=True)
    return df["trie_res"].values.tolist()
