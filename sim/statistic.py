import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .event_handler import Packet


def timeavg(arr):
    arr.sort(key=lambda entry: entry[0])
    if len(arr) > 1:
        total_time = arr[-1][0] - arr[0][0]
        accum = sum((arr[i][0] - arr[i - 1][0]) * arr[i - 1][1] for i in
                    range(1, len(arr)))
        return accum / total_time
    else:
        return 0



class Statistics:
    """Statistics of simulation"""
    def __init__(self, num_nodes):
        self._delays = [[] for i in range(num_nodes)]
        self._e2e_delays = [[] for i in range(num_nodes)]
        self._queue_size = [[] for i in range(num_nodes)]
        self._packet_loss = [[] for i in range(num_nodes)]
        self._system_size = [[] for i in range(num_nodes)]
        self._server_status = [[] for i in range(num_nodes)]

    def write_delays(self, index: int, current_time: float, packet: 'Packet'):
        self._delays[index].append(current_time - packet.created_at)
        if packet.tx_addr == 0:
            self._e2e_delays[index].append(current_time - packet.created_at)

    def write_queue_size(self, index: int, sim_time: float, new_size: int):
        self._queue_size[index].append((sim_time, new_size))

    def write_packet_loss(self, index: int, sim_time: float, packet: 'Packet'):
        self._packet_loss[index].append((sim_time, packet))

    def write_system_size(self, index, sim_time: int, new_size: int):
        self._system_size[index].append((sim_time, new_size))

    def write_server_status(self, index: int, sim_time: float, busy: bool):
        self._server_status[index].append((sim_time, 1 if busy else 0))

    def get_average_delay(self, index: int) -> np.ndarray:
        return np.asarray(self._delays[index]).mean()

    def get_average_e2e_delay(self, index: int) -> np.ndarray:
        return np.asarray(self._e2e_delays[index]).mean()

    def get_average_queue_size(self, index: int) -> np.ndarray:
        return timeavg(self._queue_size[index])

    def get_average_system_size(self, index: int) -> np.ndarray:
        return timeavg(self._system_size[index])

    def get_average_busy_ratio(self, index: int) -> np.ndarray:
        return timeavg(self._server_status[index])
