from collections import namedtuple

import numpy as np

Event = namedtuple('Event', ('event_type', 'tx_addr', 'rx_addr', 'timestamp'))


class Schedule:
    """ Event time schedule"""
    def __init__(self, num_nodes):
        self._next_packet_arrival = np.array([np.nan] * num_nodes)
        self._next_packet_receiver = np.array([np.nan] * num_nodes)
        self._next_service_end = np.array([np.nan] * num_nodes)

    def set_next_packet_arrival(self, node_index: int, sim_time: float,
                                interval: float):
        self._next_packet_arrival[node_index] = sim_time + interval

    def set_next_packet_receiver(self, node_index: int, receiver: int):
        self._next_packet_receiver[node_index] = receiver

    def set_next_service_end(self, node_index: float, sim_time: float,
                             interval: float):
        self._next_service_end[node_index] = sim_time + interval

    def has_more_events(self):
        ends = [t for t in self._next_service_end if t is not None]
        return len(ends) > 0 or self._next_packet_arrival is not None

    def next_event(self, sim_time: float):
        """
        The next closest event to simulation time will be selected.
        Parameters
        ----------
        sim_time - current simulation time

        Returns
        -------
        next event (ARRIVAL or SERVICE_END)
        """
        ev_type = 'ARRIVAL'
        if any(np.isfinite(self._next_packet_arrival)) is True:
            min_t = np.nanmin(self._next_packet_arrival)
            i, = np.where(self._next_packet_arrival == min_t)
            index = i[0]
            rx_addr = int(self._next_packet_receiver[index])
        else:
            min_t = None
            index = None
            rx_addr = None

        for i, t in enumerate(self._next_service_end):
            if not np.isnan(t):
                if (min_t is None) or (t < min_t):
                    min_t, ev_type, index = t, 'SERVICE_END', i

        # We also need to clear the event we found, so
        # it is not fired in the past the next time:

        if min_t:
            if ev_type == 'ARRIVAL':
                self._next_packet_arrival[index] = np.nan
                self._next_packet_receiver[index] = np.nan
            else:
                self._next_service_end[index] = np.nan
            return Event(ev_type, index, rx_addr, min_t)
        return Event('STOP', None, None, sim_time)
