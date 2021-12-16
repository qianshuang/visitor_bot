# -*- coding: utf-8 -*-

import string
import re


def open_file(filename, mode='r'):
    return open(filename, mode, encoding='utf-8', errors='ignore')


def read_file(filename):
    return [line.strip() for line in open(filename).readlines()]


def write_file(filename, content):
    open_file(filename, mode="w").write(content)


def write_lines(filename, list_res):
    test_w = open_file(filename, mode="w")
    for j in list_res:
        test_w.write(j + "\n")


def pre_process(query):
    # 1. 转小写
    query = query.lower()

    # 2. 去标点
    for c in string.punctuation:
        query = query.replace(c, "")

    # 3. 合并空格
    query = re.sub(r'\s+', ' ', query)
    return query
