"""
A tandem queueing model of a wireless network with a cross-traffic.
"""
import time
import json

from itertools import product


import pandas as pd
import numpy as np
import progressbar


from sim.simulation import simulate


def run(data):

    with open('input.json') as json_file:
        input_data = json.load(json_file)

    _product = list(product([input_data["SIMULATION_TYPE"]], input_data["NUM_STATIONS"],
                            input_data["BITRATE"], input_data["QUEUE_CAPACITY"],
                            input_data["MEAN_ARRIVAL_TIME"], input_data["STD_ARRIVAL_TIME"],
                            input_data["MEAN_PACKET_SIZE"], input_data["STD_PACKET_SIZE"]))


    columns = ['sim_type', 'NUM_STATIONS', 'BITRATE', 'QUEUE_CAPACITY',
               'MEAN_ARRIVAL_TIME', 'STD_ARRIVAL_TIME', 'MEAN_PACKET_SIZE',
               'STD_PACKET_SIZE', 'END2END_DELAY']

    output = np.zeros([len(data), 1])
    i = 0
    bar = progressbar.ProgressBar(maxval=len(data)).start()
    bar.update(i)
    for i in range(len(data)):
        print(i)
        (sim_type, num_stations, bitrate, queue_capacity, mean_arrival_time,
         std_arrival_time, mean_packet_size, std_packet_size) = data[i].values()
        _input = {
            'sta_where_packets_arrive': input_data['STA_WHERE_PACKETS_ARRIVE'],
            'simulation_type': sim_type == "FIXED_PACKET_SIZE",
            'num_generated_packets': input_data["NUM_GENERATED_PACKETS"],
            'mode': input_data['MODE'],
            'num_stations': num_stations,
            'queue_capacity': queue_capacity,
            'mean_arrival_time': mean_arrival_time,
            'std_arrival_time': std_arrival_time,
            'bitrate': bitrate,
            'mean_packet_size': mean_packet_size,
            'std_mean_packet_size': std_packet_size}
        stat = simulate(_input)
        output[i, :] = stat['e2e_delay'][-1]
        i += 1
        bar.update(i)
        # print('Delay {}'.format(stat['delay']))
        # print('End to End delay {}'.format(stat['e2e_delay']))

    bar.finish()

    _dataframe = np.hstack((np.array(_product), output))

    table = pd.DataFrame(_dataframe, columns=columns)
    return table.to_json('train_sample.json', orient='records')


if __name__ == "__main__":
    start_time = time.time()
    run('data.json')
    print('=== Time is {} seconds ==='.format(time.time() - start_time))