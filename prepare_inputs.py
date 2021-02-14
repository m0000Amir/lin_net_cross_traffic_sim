import json
from itertools import product


def prepare_inputs():
    with open('input.json') as json_file:
        data = json.load(json_file)

    _product = list(product([data["STA_WHERE_PACKETS_ARRIVE"]],
                            [data["SIMULATION_TYPE"]],
                            [data["NUM_GENERATED_PACKETS"]],
                            [data["MODE"]],
                            data["NUM_STATIONS"],
                            data["BITRATE"], data["QUEUE_CAPACITY"],
                            data["MEAN_ARRIVAL_TIME"], data["STD_ARRIVAL_TIME"],
                            data["MEAN_PACKET_SIZE"], data["STD_PACKET_SIZE"]))
    print(f'Number of samples: {len(_product)}')
    column = ["STA_WHERE_PACKETS_ARRIVE", "SIMULATION_TYPE",
              "NUM_GENERATED_PACKETS", "MODE", "NUM_STATIONS", "BITRATE",
              "QUEUE_CAPACITY", "MEAN_ARRIVAL_TIME", "STD_ARRIVAL_TIME",
              "MEAN_PACKET_SIZE", "STD_PACKET_SIZE"]
    mass = [None] * len(_product)
    for i in range(len(_product)):
        mass[i] = dict(zip(column, _product[i]))

    with open('data.json', 'w') as outfile:
        json.dump(mass, outfile)


if __name__ == '__main__':
    prepare_inputs()
