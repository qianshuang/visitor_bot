# -*- coding: utf-8 -*-

import Levenshtein

k = "i wodner if i can apply for latin honors"
query = "I wodner if I cann"

print(k[:len(query)])
score = Levenshtein.ratio(k[:len(query)], query)
print(score)

print(Levenshtein.ratio("i wodner if i can", "I wodner if I cann"))
