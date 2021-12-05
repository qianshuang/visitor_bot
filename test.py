# -*- coding: utf-8 -*-

import re

data = "Hello, I am Adam. How can I change password"
print(re.split(r'[,|.]', data)[-1])
