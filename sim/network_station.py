from collections import deque


class Node:
    """
    Node of a queueing network model. For this case it is a base station.
    """
    def __init__(self, index, queue_capacity):
        self.queue = deque()
        self.queue_capacity = queue_capacity
        self.server = None
        self._index = index
        self.served_packets_fingerprint = 0

    @property
    def server_busy(self):
        return self.server is not None

    @property
    def server_ready(self):
        return self.server is None

    @property
    def queue_size(self):
        return len(self.queue)

    @property
    def num_packets_in_servers(self):
        return 1 if self.server_busy else 0

    @property
    def system_size(self):
        return self.queue_size + self.num_packets_in_servers

    @property
    def index(self):
        return self._index


class State:
    """
    Network state description
    """
    def __init__(self, num_nodes: int, queue_capacity=None) -> None:
        self.arrival_packet_times = None
        self.arrival_packet_receivers = None
        self._arrival_index = 0
        self.service_packet_times = None
        self._service_index = 0
        self.nodes = []
        self.num_packets_generated = 0
        self.seqn = 0
        self.nodes = [Node(i, queue_capacity) for i in range(num_nodes)]

    @property
    def get_arrival_times_index(self) -> int:
        return self._arrival_index

    def next_arrival_times_index(self):
        self._arrival_index += 1

    @property
    def get_service_times_index(self) -> int:
        return self._service_index

    def next_service_times_index(self):
        current_index = self._service_index
        self._service_index += 1
        return current_index
