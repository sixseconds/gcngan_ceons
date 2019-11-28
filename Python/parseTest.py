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
DATA_FOLDER = "../Test_Data/"

with open("../Yml/topology.yml") as file:
    data = yaml.load(file, Loader=loader)
    nodes = [node["name"] for node in data["nodes"]]
    topology.add_nodes_from(nodes)
    links = [key for key in list(data["links"].keys())]

topology.add_edges_from(links)
for index, link in enumerate(links):
    topology[link[0]][link[1]]["length"] = data["links"][link]["length"]

# print(topology.nodes)
# print(topology.edges)

# adj = nx.adjacency_matrix(topology)
# identity = np.identity(26)
# a_ca = adj + identity

# print(nx.normalized_laplacian_matrix(topology).A)


def calc_weight(source, destination, edge):
    return edge.get("volTTL") * edge.get("length")


# file_name = ""

# while file_name != "q":
#     file_name = input(
#         "Burst Pattern:\n(s - single burst, d - double burst, p - plateau)\n"
#     )
#     if file_name == "s" or file_name == "d" or file_name == "p":
#         break
#     else:
#         print("Please enter s, d, or p")

# if file_name == "s":
#     file_name = "single_burst"
# elif file_name == "d":
#     file_name = "double_burst"
# else:
#     file_name = "plateau"

file_names = ["single_burst", "double_burst", "plateau"]


def main():
    for file_name in file_names:
        with open(DATA_FOLDER + file_name + ".csv", newline="") as burst_file:
            demands = csv.reader(burst_file)
            network_demands = []
            data_list = -1

            for index, row in enumerate(demands):
                for link in links:
                    topology[link[0]][link[1]]["volTTL"] = 1

                source, destination, vol, ttl = row
                vol, ttl = int(vol), int(ttl)
                shortest_path = nx.dijkstra_path(
                    topology, source, destination, weight=calc_weight
                )

                path_edges = []
                while len(shortest_path) > 1:
                    src_node = shortest_path.pop(0)
                    path_edges.append([src_node, shortest_path[0]])

                network_demands.append([path_edges, vol, ttl])
                for demand in network_demands:
                    demand[2] -= 1
                network_demands = [
                    demand for demand in network_demands if demand[2] > 0
                ]
                # print(len(network_demands))

                for demand in network_demands:
                    for edge in demand[0]:
                        if topology[edge[0]][edge[1]]["volTTL"] == 1:
                            topology[edge[0]][edge[1]]["volTTL"] = demand[1] * demand[2]
                        else:
                            topology[edge[0]][edge[1]]["volTTL"] += (
                                demand[1] * demand[2]
                            )

                if index % 60 == 0:
                    data_list += 1
                    with open(
                        f"data\{file_name}\edge_list_{data_list}.txt", "w+"
                    ) as file:
                        for node, data_dict in topology.adj.items():
                            for nbr, length_dict in data_dict.items():
                                data_line = " ".join(
                                    [
                                        str(node)[5::],
                                        str(nbr)[5::],
                                        str(topology[node][nbr]["volTTL"]),
                                    ]
                                )
                                file.write(f"{data_line}\n")
                    print(data_list)


if __name__ == "__main__":
    main()
