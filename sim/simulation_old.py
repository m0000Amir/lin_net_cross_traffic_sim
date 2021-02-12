# # :TODO: Remove module
# import numpy as np
#
# from sim.network_station import State
# from sim.event import Schedule
# from sim.statistic import Statistics
# from sim.event_handler import handle_packet_arrival, handle_service_finished
#
#
# def initialize(sim_time, schedule, state, params):
#     """
#     Prepare of arrival packets
#     :param sim_time: simulation time
#     :param schedule: event schedule
#     :param state: state model
#     :param params: simulation params
#     :return: schedule.set_next_packet_arrival()
#     """
#     assert type(params['arrive_pkt_dist_shape']) is int, (
#         'Shape must be integer. Erlang distribution')
#
#     if params['sta_where_pkt_arrive'] is -1:
#         """ Packets arrive at all stations"""
#         for i in range(len(state.nodes)):
#             schedule.set_next_packet_arrival(
#                 i,
#                 sim_time,
#                 np.random.gamma(shape=params['arrive_pkt_dist_shape'],
#                                 scale=(params['mean_arrival_interval'] /
#                                        params['arrive_pkt_dist_shape']))
#             )
#     else:
#         """ Packets arrive at the only station[index] """
#         index = params['sta_where_pkt_arrive']
#         for i in index:
#             schedule.set_next_packet_arrival(
#                 i,
#                 sim_time,
#                 np.random.gamma(shape=params['arrive_pkt_dist_shape'],
#                                 scale=(params['mean_arrival_interval'] /
#                                        params['arrive_pkt_dist_shape']))
#             )
#
#
# def simulate(num_nodes: float, mean_arrival_interval: float,
#              mean_packet_size: float, bitrate: float,
#              num_packets: float, arrive_pkt_dist_shape: int = 1,
#              pktsize_dist_shape: int = 1, fixed_packet_size: bool = True,
#              sta_where_pkt_arrive: None = None) -> dict:
#     """
#     To simulate model
#
#     :param num_nodes: Number of station
#     :param mean_arrival_interval: Distribution parameter
#     :param mean_packet_size:
#     :param bitrate:
#     :param num_packets: Number of generated packets
#     :param arrive_pkt_dist_shape: shape of Gamma distribution for arrival
#     interval
#     :param pktsize_dist_shape: shape of Gamma distribution for packet size
#     :param fixed_packet_size: True -> if all arrival packets have fixed size,
#                               False -> otherwise
#     :param sta_where_pkt_arrive: Packets arrive at the only this stations
#     :return: delay
#     """
#     params = {
#         'mean_arrival_interval': mean_arrival_interval,
#         'mean_packet_size': mean_packet_size,
#         'bitrate': bitrate,
#         'fixed_packet_size': fixed_packet_size,
#         'num_packets': num_packets,
#         'arrive_pkt_dist_shape': arrive_pkt_dist_shape,
#         'pktsize_dist_shape': pktsize_dist_shape,
#         'sta_where_pkt_arrive': sta_where_pkt_arrive
#     }
#     state = State(num_nodes)
#     schedule = Schedule(num_nodes)
#     statistics = Statistics(num_nodes)
#
#     sim_time = 0.0
#
#     initialize(sim_time, schedule, state, params)
#
#     while True:
#         event = schedule.next_event(sim_time)
#         sim_time = event.timestamp
#         if event.event_type == 'ARRIVAL':
#             handle_packet_arrival(sim_time, state, event.index,
#                                   statistics, schedule, params)
#         elif event.event_type == 'SERVICE_END':
#             handle_service_finished(sim_time, state, event.index,
#                                     statistics, schedule, params)
#         else:
#             break
#
#     stat = {
#         'delay': [statistics.get_average_delay(i) for i in range(num_nodes)],
#         # 'qsize': [statistics.get_average_queue_size(i) for i in
#         #           range(num_nodes)],
#         # 'ssize': [statistics.get_average_system_size(i) for i in
#         #           range(num_nodes)],
#         # 'busy': [statistics.get_average_busy_ratio(i) for i in
#         #          range(num_nodes)],
#         # 'fingerprint': [state.nodes[i].served_packets_fingerprint for i in
#         #                 range(num_nodes)],
#     }
#
#     b = 1,
#     return stat
