#!/usr/bin/env python
__author__ = 'Albino'

import re

rule = '\d+/#pvareaid=\d+'
r = re.findall('ah-100/',rule)
print(r)