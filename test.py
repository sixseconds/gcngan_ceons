#!/usr/bin/env python3-64

from __future__ import absolute_import, division, print_function, unicode_literals

# Install TensorFlow

import tensorflow as tf
import numpy as np
import networkx as nx

import yaml

from node import Node
from datacenter import Datacenter

loader = yaml.Loader

topology = nx.Graph()

with open("./topology.yml") as file:
    data = yaml.load(file, Loader=loader)
    nodes = [
        # Node(node["location"], node["xcoordinate"], node["ycoordinate"])
        node["name"]
        for node in data["nodes"]
    ]
    locations = [node["location"] for node in data["nodes"]]
    # print(nodes)
    topology.add_nodes_from(nodes)
    for node in topology.nodes():
        topology.nodes[node]["location"] = locations[node]

    print(topology.nodes())

    DCS = []
    for group, members in data["groups"].items():
        DCS.extend(members)

    # print(topology.nodes())
    for dc in DCS:
        topology.nodes[dc]["cpu"] = 8
        topology.nodes[dc]["ram"] = 8
        topology.nodes[dc]["storage"] = 8

    print(topology.nodes(data=True))

    links = [(key[0], key[1]) for key in list(data["links"].keys())]
    # print(links)
    topology.add_edges_from(links)
    # print(len(topology.edges()))
    adj = nx.adjacency_matrix(topology)
    identity = np.identity(26)
    a_ca = adj + identity

    print(nx.normalized_laplacian_matrix(topology).A)
