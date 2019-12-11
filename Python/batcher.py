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
    return edge.get("volTTL") * edge.get("length")


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


def single_burst():
    print('batching single_burst')
    single_burst = []
    single_burst.extend(random.choices([0, 1], k=56))
    single_burst.extend(random.choices([1, 2], k=7))
    single_burst.extend(random.choices([2, 3, 4], weights=[1, 2, 3], k=7))
    single_burst.extend(random.choices([3, 4, 5], weights=[1, 1, 2], k=14))
    single_burst.extend(random.choices([4, 5], weights=[1, 2], k=14))
    single_burst.extend(random.choices([3, 4, 5], weights=[2, 1, 1], k=14))
    single_burst.extend(random.choices([1, 2, 3, 4], weights=[3, 2, 1, 1], k=28))
    single_burst.extend(random.choices([0, 1, 2], weights=[3, 2, 1], k=29))

    single_burst = [erlangs[val] for val in single_burst]

    with open("../Test_Data/single_burst.csv", "w+") as test:
        for load in single_burst:
            with open(random.choice(files[load])) as erlCSV:
                requests = erlCSV.readlines()
                rand_requests = random.sample(requests, 60)
                for req in rand_requests:
                    test.write(req)
    return single_burst


def double_burst():
    print('batching double_burst')
    double_burst = []
    double_burst.extend(random.choices([0, 1], k=56))
    double_burst.extend(random.choices([1, 2, 3], weights=[1, 1, 2], k=7))
    double_burst.extend(random.choices([3, 4, 5], weights=[1, 2, 3], k=14))
    double_burst.extend(random.choices([2, 3, 4], weights=[1, 1, 2], k=14))
    double_burst.extend(random.choices([4, 5, 6], weights=[1, 1, 2], k=7))
    double_burst.extend(random.choices([6, 7], weights=[1, 2], k=14))
    double_burst.extend(random.choices([3, 4, 5, 6], weights=[3, 2, 1, 1], k=14))
    double_burst.extend(random.choices([1, 2, 3, 4], weights=[3, 2, 1, 1], k=21))
    double_burst.extend(random.choices([0, 1, 2], weights=[3, 2, 1], k=22))

    double_burst = [erlangs[val] for val in double_burst]
    with open("../Test_Data/double_burst.csv", "w+") as test:
        for load in double_burst:
            with open(random.choice(files[load])) as erlCSV:
                requests = erlCSV.readlines()
                rand_requests = random.sample(requests, 60)
                for req in rand_requests:
                    test.write(req)
    return double_burst


def plateau():
    print('batching plateau')
    plateau = []
    plateau.extend(random.choices([0, 1], k=21))
    plateau.extend(random.choices([1, 2], k=21))
    plateau.extend(random.choices([2, 3, 4], weights=[1, 2, 3], k=21))
    plateau.extend(random.choices([3, 4, 5], weights=[1, 1, 2], k=21))
    plateau.extend(random.choices([4, 5], weights=[1, 2], k=21))
    plateau.extend(random.choices([3, 4, 5], weights=[2, 1, 1], k=21))
    plateau.extend(random.choices([1, 2, 3, 4], weights=[3, 2, 1, 1], k=21))
    plateau.extend(random.choices([0, 1, 2], weights=[3, 2, 1], k=22))

    plateau = [erlangs[val] for val in plateau]
    with open("../Test_Data/plateau.csv", "w+") as test:
        for load in plateau:
            with open(random.choice(files[load])) as erlCSV:
                requests = erlCSV.readlines()
                rand_requests = random.sample(requests, 60)
                for req in rand_requests:
                    test.write(req)
    return plateau

def bigBatch():
    big_batch = []
    func_names = [single_burst, double_burst, plateau]
    
    weeks = 12
    for i in range(weeks):
        print('Batch ' + str(i+1) + '/' + str(weeks))
        big_batch.extend(func_names[random.randint(0, 2)]())

    print('writing to batch file')
    with open("../Test_Data/bigBatch.csv", "w+") as test:
        for load in big_batch:
            with open(random.choice(files[load])) as erlCSV:
                requests = erlCSV.readlines()
                rand_requests = random.sample(requests, 60)
                for req in rand_requests:
                    test.write(req)
    return big_batch

def main(): 
    # single_burst()
    # double_burst()
    # plateau()
    bigBatch()

if __name__ == "__main__":
    main()