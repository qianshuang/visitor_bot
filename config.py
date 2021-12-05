# -*- coding: utf-8 -*-

import marisa_trie
import schedule
import hashlib
import os
import json
import re
from collections import Counter

from common import *

# 默认返回大小
default_size = 10

# 每小时加载intents文件
INTENT_FILE = "data/intents.txt"
md5_intent_ori = hashlib.md5(open(INTENT_FILE).read().encode("utf-8")).hexdigest()
# 构建原始标准问映射
intents_lower_dict = {intent.lower(): intent for intent in read_file(INTENT_FILE)}
# 构建Trie树
trie = marisa_trie.Trie(list(intents_lower_dict.keys()))
print("intents trie finished building...")


def run_intents():
    if hashlib.md5(open(INTENT_FILE).read().encode("utf-8")).hexdigest() != md5_intent_ori:
        intents_lower_dict.clear()
        for intent in read_file(INTENT_FILE):
            intents_lower_dict[intent.lower()] = intent
        # global trie
        globals()['trie'] = marisa_trie.Trie(list(intents_lower_dict.keys()))


schedule.every().hour.do(run_intents)

# 每小时加载priority文件，越top优先级越高
PRIORITY_FILE = "data/priority.txt"
md5_ori = hashlib.md5(open(PRIORITY_FILE).read().encode("utf-8")).hexdigest()
priorities = read_file(PRIORITY_FILE)
print("priority file finished loading...")


def run():
    if hashlib.md5(open(PRIORITY_FILE).read().encode("utf-8")).hexdigest() != md5_ori:
        # global priorities
        priorities.clear()
        priorities.extend(read_file(PRIORITY_FILE))


schedule.every().hour.do(run)

# 读取recent文件，越top优先级越高
RECENT_FILE = "data/recent.txt"
if not os.path.exists(RECENT_FILE):
    recents = []
else:
    recents = read_file(RECENT_FILE)
print("recent file finished loading...")

# 读取frequency文件
FREQUENCY_FILE = "data/frequency.json"
if not os.path.exists(FREQUENCY_FILE):
    frequency = {}
else:
    with open(FREQUENCY_FILE, encoding="utf-8") as f:
        frequency = json.load(f)
print("frequency file finished loading...")


# 单词纠错
def words(text):
    return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('data/big.txt').read()))
print("vocab file finished loading...")


def P(word, N=sum(WORDS.values())):
    """Probability of `word`."""
    return WORDS[word] / N


def correction(word):
    """Most probable spelling correction for word."""
    return max(candidates(word), key=P)


def candidates(word):
    """Generate possible spelling corrections for word."""
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words_):
    """The subset of `words` that appear in the dictionary of WORDS."""
    return set(w for w in words_ if w in WORDS)


def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
