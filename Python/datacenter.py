from node import Node


class Datacenter(Node):
    def __init__(self, name, x_coordinate, y_coordinate, cpu=8, ram=30, storage=120):
        super().__init__(name, x_coordinate, y_coordinate)
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

