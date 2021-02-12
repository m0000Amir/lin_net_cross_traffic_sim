from queue_model.arrival import get_arrival_times, get_arrival_packet_receivers
from queue_model.service import get_service_times
from sim.network_station import State
from sim.event import Schedule
from sim.statistic import Statistics
from sim.event_handler import handle_packet_arrival, handle_service_finished


from collections import namedtuple


Packet = namedtuple('Packet', ('created_at', 'size', 'seqn',
                               'tx_addr', 'rx_addr'))


def initialize(sim_time: float, schedule: Schedule, state: State,
               params: dict) -> None:
    """
    Initialize arrival packets to start simulation.

    Parameters
    ----------
    sim_time : simulation time
    schedule : event schedule
    state : state model
    params : simulation parameters
    """

    state.arrival_packet_times = get_arrival_times(params)
    state.service_packet_times = get_service_times(params)
    state.arrival_packet_receivers = get_arrival_packet_receivers(params)

    if params['sta_where_packets_arrive'] is -1:
        """ Packets arrive at all stations"""
        for i in range(len(state.nodes)):
            # arrival_index = state.arrival_times_index
            schedule.set_next_packet_arrival(
                i,
                sim_time,
                state.arrival_packet_times[state.get_arrival_times_index]
            )
            schedule.set_next_packet_receiver(
                i,
                state.arrival_packet_receivers[state.get_arrival_times_index]
            )
            state.next_arrival_times_index()
    else:
        """ Packets arrive at the only station[index] """
        index = params['sta_where_packets_arrive']
        for i in index:
            schedule.set_next_packet_arrival(
                i,
                sim_time,
                state.arrival_packet_times[state.get_arrival_times_index]
            )
            schedule.set_next_packet_receiver(
                i,
                state.arrival_packet_receivers[state.get_arrival_times_index]
            )
            state.next_arrival_times_index()


def simulate(_input: dict) -> dict:
    """
    Simulation model of queueing system

    Parameters
    ----------
    _input : contains simulation input data

    Returns
    -------
        end-to-end delay of tandem network

    """

    params = _input

    state = State(params['num_stations'], params['queue_capacity'])
    schedule = Schedule(params['num_stations'])
    statistics = Statistics(params['num_stations'])

    sim_time = 0.0

    initialize(sim_time, schedule, state, params)

    while True:
        event = schedule.next_event(sim_time)
        sim_time = event.timestamp
        if event.event_type == 'ARRIVAL':
            handle_packet_arrival(sim_time, state, event.tx_addr, event.rx_addr,
                                  statistics, schedule, params)
        elif event.event_type == 'SERVICE_END':
            handle_service_finished(sim_time, state, event.tx_addr,
                                    statistics, schedule, params)
        else:
            break

    stat = {
        'delay': [statistics.get_average_delay(i)
                  for i in range(params['num_stations'])],
        'e2e_delay': [statistics.get_average_e2e_delay(i)
                      for i in range(params['num_stations'])],
    }
    return stat
