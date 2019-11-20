#!/usr/bin/env python3-64

import json
import os
import sys


with open(f"../Test_Data/From_Liam/REAL-DATA-1/US26_2019_11_14_16_22_52_demands.json") as file:
    data = json.load(file)
    demands = [key[list(key.keys())[0]] for key in data]
    
    
    batch = []
    for tick in range(200):
        demand = demands[tick]
        demand["initialttl"] -= (200-tick)
        if (demand["initialttl"] > 0):
            batch.append(demand)

    print(batch)
