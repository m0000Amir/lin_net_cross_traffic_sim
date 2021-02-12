from sim.network_station import State, Node
from sim.event import Schedule


from sim.statistic import Statistics


from collections import namedtuple

Packet = namedtuple('Packet', ('created_at', 'size', 'seqn',
                               'tx_addr', 'rx_addr'))


def handle_packet_arrival(sim_time: int, state: State, tx_addr: int,
                          rx_addr: int, statistics: Statistics,
                          schedule: Schedule, params: dict):
    """
    The handler of  arrival packets

    Parameters
    ----------
    sim_time: Current simulation time
    state: Network state
    tx_addr: Node in which the packet arrived
    rx_addr: Node to which the package should be delivered
    statistics: Statistics of simulation
    schedule: Event time schedule
    params: input parameters

    """
    if params['simulation_type']:
        pkt_size = state.service_packet_times[state.get_service_times_index]
        state.next_service_times_index()
    else:
        pkt_size = None

    pkt = Packet(sim_time, pkt_size, state.seqn, tx_addr, rx_addr)

    send(sim_time, state.nodes[tx_addr], pkt, statistics, schedule, params)
    state.seqn += 1
    state.num_packets_generated = state.get_arrival_times_index + 1
    if state.num_packets_generated < params['num_generated_packets']:
        schedule.set_next_packet_arrival(
            tx_addr,
            sim_time,
            state.arrival_packet_times[state.get_arrival_times_index]
        )
        schedule.set_next_packet_receiver(
            tx_addr,
            state.arrival_packet_receivers[state.get_arrival_times_index]
        )
        state.next_arrival_times_index()


def handle_service_finished(sim_time: int, state: State, tx_addr: int,
                            statistics: Statistics, schedule: Schedule,
                            params: dict):
    """
    The handler of  serviced packets

    Parameters
    ----------
    sim_time: Current simulation time
    state: Network state
    tx_addr: Node in which the packet arrived
    statistics: Statistics of simulation
    schedule: Event time schedule
    params: input parameters

    """
    node = state.nodes[tx_addr]
    pkt = node.server
    node.server = None

    if pkt.rx_addr > tx_addr:
        send(sim_time, state.nodes[tx_addr + 1], pkt, statistics, schedule,
             params)
    elif pkt.rx_addr < tx_addr:
        send(sim_time, state.nodes[tx_addr - 1], pkt, statistics, schedule,
             params)

    statistics.write_delays(tx_addr, sim_time, pkt)

    if node.queue:
        pkt = node.queue.popleft()
        statistics.write_queue_size(tx_addr, sim_time, node.queue_size)
        start_service(sim_time, node, pkt, schedule, params)
    else:
        statistics.write_server_status(tx_addr, sim_time, False)

    statistics.write_system_size(tx_addr, sim_time, node.system_size)


def start_service(sim_time: int, node: Node, pkt: Packet, schedule: Schedule,
                  params: dict):
    """
    Starting of service in node

    Parameters
    ----------
    sim_time: Current simulation time
    node: Network node
    pkt: Packet which should be serviced
    schedule: Event time schedule
    params: input parameters

    """
    node.server = pkt
    if pkt.size:
        pkt_size = pkt.size
    else:
        # TODO: change for this case
        pkt_size = pkt.size
        assert type(params['pktsize_dist_shape']) is int, (
            'Shape must be integer. Erlang distribution')

    schedule.set_next_service_end(node.index, sim_time,
                                  pkt_size/params['bitrate'])
    node.served_packets_fingerprint = (node.served_packets_fingerprint +
                                       pkt_size * (pkt.seqn % 37)) % 9973


def send(sim_time: int, node: Node, pkt: Packet, statistics: Statistics,
         schedule: Schedule, params: dict):
    if node.server_busy:
        if node.queue_capacity is None or \
                len(node.queue) < node.queue_capacity:
            node.queue.append(pkt)
            statistics.write_queue_size(node.index, sim_time, node.queue_size)
        else:
            statistics.write_packet_loss(node.index, sim_time, pkt)
    else:
        start_service(sim_time, node, pkt, schedule, params)
        statistics.write_server_status(node.index, sim_time, True)
    statistics.write_system_size(node.index, sim_time, node.system_size)
