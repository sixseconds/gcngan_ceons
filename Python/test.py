#!/usr/bin/env python3-64

from __future__ import absolute_import, division, print_function, unicode_literals

# Install TensorFlow

import tensorflow as tf
import numpy as np
import networkx as nx

import json
import os
import sys


import yaml

from node import Node
from datacenter import Datacenter

loader = yaml.Loader

topology = nx.Graph()

LABEL_END = '_erlang'

with open("../Yml/topology.yml") as file:
    data = yaml.load(file, Loader=loader)
    nodes = [
        # Node(node["location"], node["xcoordinate"], node["ycoordinate"])
        node["name"]
        for node in data["nodes"]
    ]

    # print(nodes)
    topology.add_nodes_from(nodes)
    for node in nodes:
        topology.nodes[node]["volTTL"] = 0

    # print(topology.nodes())

    # print(data["links"])
    links = [key for key in list(data["links"].keys())]
    # print(links)
    topology.add_edges_from(links)
    for link in links:
        topology[link[0]][link[1]]["weight"] = data["links"][link]["length"]

    # adj = nx.adjacency_matrix(topology)
    # identity = np.identity(26)
    # a_ca = adj + identity

    # print(nx.normalized_laplacian_matrix(topology).A)

    def calc_weight(source, destination, edge):
        source_vol_ttl = topology.nodes[source].get("volTTL")
        destination_vol_ttl = topology.nodes[destination].get("volTTL")
        edge_length = edge.get("weight")

        return (source_vol_ttl + destination_vol_ttl) * edge_length

    with open(
        f"../Test_Data/From_Liam/REAL-DATA-1/US26_2019_11_14_16_22_52_demands.json"
    ) as file:
        data = json.load(file)
        demands = [key[list(key.keys())[0]] for key in data]

        batch = []
        for tick in range(180):
            demand = demands[tick + 3000]
            demand["initialttl"] -= 180 - tick
            if demand["initialttl"] > 0:
                batch.append(demand)

        parsed = []
        for demand in batch:
            erl = demand["initialttl"] * demand["volume"]

            if "source" in demand:
                shortest_path = nx.dijkstra_path(
                    topology, demand["source"]["name"], demand["destination"]["name"], weight=calc_weight
                )

                for node in shortest_path:
                    topology.nodes[node]["volTTL"] += erl
            # else:
            #     for node in nodes:
            #         nodes[node] += erl

        # print(topology.nodes(data=True))
        # for node in topology.nodes(data=True):
        #     print(node[0])
        #     print(node[1]['volTTL'])

        # for edge in topology.edges:
        #     print(edge)

        with open("featureLabelData.content", "w") as file:
            for node in topology.nodes(data=True):
                if node[1]['volTTL'] > 2500000:
                    erl = '1000'
                elif node[1]['volTTL'] > 2000000:
                    erl = '900'
                elif node[1]['volTTL'] > 1500000:
                    erl = '800' 
                elif node[1]['volTTL'] > 1000000:
                    erl = '700' 
                elif node[1]['volTTL'] > 950000:
                    erl = '600'
                elif node[1]['volTTL'] > 900000:
                    erl = '500'
                elif node[1]['volTTL'] > 850000:
                    erl = '400'
                else:
                    erl = '300'     
                file.write("{} {} {}\n".format(node[0][5:], node[1]['volTTL'], (erl + LABEL_END)))

        with open("edges.cites", "w") as file:
            for edge in topology.edges:
                file.write("{} {}\n".format(edge[0][5:], edge[1]))

