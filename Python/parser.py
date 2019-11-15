#!/usr/bin/env python3-64

import json
import os
import sys

with open("US26_2019_11_11_18_14_54.json") as file:
    data = json.load(file)
    print(len(data))
