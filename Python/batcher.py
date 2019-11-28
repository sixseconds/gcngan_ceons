#!/usr/bin/env python3-64

from __future__ import absolute_import, division, print_function, unicode_literals

# Install TensorFlow

import numpy as np
import networkx as nx

import json
import os
import sys

import csv
import yaml

loader = yaml.Loader

topology = nx.Graph()

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
        topology[link[0]][link[1]]["demands"] = []

    # adj = nx.adjacency_matrix(topology)
    # identity = np.identity(26)
    # a_ca = adj + identity

    # print(nx.normalized_laplacian_matrix(topology).A)

    def calc_weight(source, destination, edge):
        source_vol_ttl = topology.nodes[source].get("volTTL")
        destination_vol_ttl = topology.nodes[destination].get("volTTL")
        edge_length = edge.get("weight")

        return (source_vol_ttl + destination_vol_ttl) * edge_length

    file_list = []
    DATA_PATH = "../Test_Data/From_Liam/REAL-DATA-1"
    for item in os.listdir(DATA_PATH):
        file_list.append(item)

    grouped_files = list(zip(file_list[::2], file_list[1::2]))

    for item in grouped_files:
        demand_file = item[0]
        erlang = 300 + (grouped_files.index(item) * 100)
        with open(os.path.join(DATA_PATH, demand_file)) as file:
            data = json.load(file)
            # print(data[0])
            demands = [key[list(key.keys())[0]] for key in data]
            net_demands = []
            # print(demands)
            for tick in range(555):
                net_demands.append(demands[tick])
                
                for node in topology.nodes:
                    topology.nodes[node]["volTTL"] = 0

                
                batch = []
                lower = tick * 180
                upper = (tick + 1) * 180
                grouped = demands[lower:upper]
                for demand in grouped:
                    demand["initialttl"] -= 180 - tick
                    if demand["initialttl"] > 0:
                        batch.append(demand)
                for demand in batch:
                    erl = demand["initialttl"] * demand["volume"]
                    if "source" in demand:
                        shortest_path = nx.dijkstra_path(
                            topology,
                            demand["source"]["name"],
                            demand["destination"]["name"],
                            weight=calc_weight,
                        )

                        for index, node in enumerate(shortest_path)):
                            if index != len(shortest_path):
                                


                        for node in shortest_path:
                            topology.nodes[node]["volTTL"] += erl

                with open(f"data\erlang_{erlang}\edge_list_{tick}.txt", "w") as file:
                    for node, data_dict in topology.adj.items():
                        for nbr, length_dict in data_dict.items():
                            data_line = " ".join(
                                [
                                    str(node)[5::],
                                    str(nbr)[5::],
                                    str(
                                        topology.nodes[node].get("volTTL")
                                        + topology.nodes[nbr].get("volTTL")
                                    ),
                                ]
                            )
                            file.write(f"{data_line}\n")
