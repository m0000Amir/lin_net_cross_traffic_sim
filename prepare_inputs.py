import json
from itertools import product

if __name__ == '__main__':
    with open('input.json') as json_file:
        data = json.load(json_file)

    _product = list(product([data["SIMULATION_TYPE"]], data["NUM_STATIONS"],
                            data["BITRATE"], data["QUEUE_CAPACITY"],
                            data["MEAN_ARRIVAL_TIME"], data["STD_ARRIVAL_TIME"],
                            data["MEAN_PACKET_SIZE"], data["STD_PACKET_SIZE"]))
    print(len(_product))
    column = ["SIMULATION_TYPE", "NUM_STATIONS", "BITRATE", "QUEUE_CAPACITY",
              "MEAN_ARRIVAL_TIME", "STD_ARRIVAL_TIME", "MEAN_PACKET_SIZE",
              "STD_PACKET_SIZE"]
    a = [None] * len(_product)
    for i in range(len(_product)):
        a[i] = dict(zip(column, _product[i]))

    with open('data.json', 'w') as outfile:
        json.dump(a, outfile)

a = 1