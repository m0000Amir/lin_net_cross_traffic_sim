import json
from itertools import product


import numpy as np


def prepare_inputs(sample_num: int) -> None:
    with open('input.json') as json_file:
        data = json.load(json_file)
    # sample_num = 20000
    swpa = np.zeros(sample_num)
    simtype = [None] * sample_num
    numgenp = np.zeros(sample_num)
    mode = [None] * sample_num
    num_sta = np.zeros(sample_num)
    bitrate = np.zeros(sample_num)
    qcapacity = np.zeros(sample_num)
    mean_a = np.zeros(sample_num)
    std_a = np.zeros(sample_num)
    mean_size = np.zeros(sample_num)
    std_size = np.zeros(sample_num)

    column = ["STA_WHERE_PACKETS_ARRIVE", "SIMULATION_TYPE",
              "NUM_GENERATED_PACKETS", "MODE", "NUM_STATIONS", "BITRATE",
              "QUEUE_CAPACITY", "MEAN_ARRIVAL_TIME", "STD_ARRIVAL_TIME",
              "MEAN_PACKET_SIZE", "STD_PACKET_SIZE"]

    mass = [0] * sample_num
    for i in range(sample_num):
        swpa[i] = data['STA_WHERE_PACKETS_ARRIVE']
        simtype[i] = data['SIMULATION_TYPE']
        numgenp[i] = data['NUM_GENERATED_PACKETS']
        mode[i] = data['MODE']
        num_sta[i] = np.random.randint(data['NUM_STATIONS'][0],
                                       data['NUM_STATIONS'][-1] + 1)
        bitrate[i] = round(np.random.uniform(data['BITRATE'][0],
                                             data['BITRATE'][-1] + 1), 3)
        qcapacity[i] = np.random.randint(data['QUEUE_CAPACITY'][0],
                                         data['QUEUE_CAPACITY'][-1] + 1)
        mean_a[i] = round(np.random.uniform(data['MEAN_ARRIVAL_TIME'][0],
                                            data['MEAN_ARRIVAL_TIME'][-1]), 3)
        std_a[i] = round(np.random.uniform(data['STD_ARRIVAL_TIME'][0],
                                           data['STD_ARRIVAL_TIME'][-1]), 3)
        mean_size[i] = round(np.random.uniform(data['MEAN_PACKET_SIZE'][0],
                                               data['MEAN_PACKET_SIZE'][-1]), 3)
        std_size[i] = round(np.random.uniform(data['STD_PACKET_SIZE'][0],
                                              data['STD_PACKET_SIZE'][-1]), 3)

        mass[i] = dict(zip(column, (int(swpa[i]),
                                    simtype[i],
                                    int(numgenp[i]),
                                    mode[i],
                                    int(num_sta[i]),
                                    bitrate[i],
                                    int(qcapacity[i]),
                                    mean_a[i],
                                    std_a[i],
                                    mean_size[i],
                                    std_size[i])))

    # _product = list(product([data["STA_WHERE_PACKETS_ARRIVE"]],
    #                         [data["SIMULATION_TYPE"]],
    #                         [data["NUM_GENERATED_PACKETS"]],
    #                         [data["MODE"]],
    #                         data["NUM_STATIONS"],
    #                         data["BITRATE"], data["QUEUE_CAPACITY"],
    #                         data["MEAN_ARRIVAL_TIME"], data["STD_ARRIVAL_TIME"],
    #                         data["MEAN_PACKET_SIZE"], data["STD_PACKET_SIZE"]))
    # print(f'Number of samples: {len(_product)}')
    # column = ["STA_WHERE_PACKETS_ARRIVE", "SIMULATION_TYPE",
    #           "NUM_GENERATED_PACKETS", "MODE", "NUM_STATIONS", "BITRATE",
    #           "QUEUE_CAPACITY", "MEAN_ARRIVAL_TIME", "STD_ARRIVAL_TIME",
    #           "MEAN_PACKET_SIZE", "STD_PACKET_SIZE"]
    # mass = [None] * len(_product)
    # for i in range(len(_product)):
    #     print(_product[i])
    #     mass[i] = dict(zip(column, _product[i]))

    with open('data.json', 'w') as outfile:
        json.dump(mass, outfile)


if __name__ == '__main__':
    SAMPLE_NUM = 20000
    prepare_inputs(SAMPLE_NUM)
