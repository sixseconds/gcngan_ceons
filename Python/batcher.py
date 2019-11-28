#!/usr/bin/env python3-64

from __future__ import absolute_import, division, print_function, unicode_literals

# Install TensorFlow

import numpy as np
import networkx as nx

import json
import os
import sys
from pathlib import Path

import random

import csv
import yaml

loader = yaml.Loader

topology = nx.Graph()
links = []

LABEL_END = "_erlang"

with open("../Yml/topology.yml") as file:
    data = yaml.load(file, Loader=loader)
    nodes = [node["name"] for node in data["nodes"]]

    topology.add_nodes_from(nodes)
    # for node in nodes:
    # topology.nodes[node]["volTTL"] = 0

    links = [key for key in list(data["links"].keys())]

topology.add_edges_from(links)
for link in links:
    topology[link[0]][link[1]]["length"] = data["links"][link]["length"]
    topology[link[0]][link[1]]["volTTL"] = 1

# print(topology.nodes)
# print(topology.edges)

# adj = nx.adjacency_matrix(topology)
# identity = np.identity(26)
# a_ca = adj + identity

# print(nx.normalized_laplacian_matrix(topology).A)


def calc_weight(source, destination, edge):
    source_vol_ttl = topology.nodes[source].get("volTTL")
    destination_vol_ttl = topology.nodes[destination].get("volTTL")
    edge_length = edge.get("weight")

    return (source_vol_ttl + destination_vol_ttl) * edge_length


files = {}
TEST_PATH = Path("../Test_Data/CSV-1")
for item in TEST_PATH.iterdir():
    if item.is_dir():
        files[f"{item.stem}"] = []
        for demands in item.iterdir():
            if demands.suffix == ".csv":
                files[f"{item.stem}"].append(demands)
erlangs = list(files.keys())
erlangs.append(erlangs.pop(0))
# print(erlangs)

# 60 * 24 * 7 = 10080 ticks per week
# 60 ticks per timeslice
# 168 slices per week

# Single burst batch
def single_burst():
    single_burst = []
    single_burst.extend(random.choices([0, 1], k=56))
    single_burst.extend(random.choices([1, 2, 3], weights=[1, 1, 2], k=7))
    single_burst.extend(random.choices([2, 3, 4, 5], weights=[1, 1, 2, 3], k=7))
    single_burst.extend(random.choices([5, 6, 7], weights=[1, 1, 2], k=7))
    single_burst.extend(random.choices([6, 7], weights=[1, 2], k=7))
    single_burst.extend(random.choices([5, 6, 7], weights=[2, 1, 1], k=14))
    single_burst.extend(random.choices([3, 4, 5, 6], weights=[3, 2, 1, 1], k=14))
    single_burst.extend(random.choices([1, 2, 3, 4], weights=[3, 2, 1, 1], k=28))
    single_burst.extend(random.choices([0, 1, 2], weights=[3, 2, 1], k=28))
    return single_burst

print(single_burst())


double_burst = []
plateau = []
