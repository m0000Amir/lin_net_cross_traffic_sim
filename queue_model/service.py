import numpy as np


from queue_model.randoms import get_random_eval


def get_service_times(params: dict) -> np.ndarray:
    """
    Prepare random variables of serviced packet size
    Parameters
    ----------
    params: input parameters

    Returns
    -------
        Vector of serviced packet sizes
    """
    average = params['mean_packet_size'] / params['bitrate']
    std = params['mean_packet_size'] / params['bitrate']
    if params['sta_where_packets_arrive'] == -1:
        treads = params['num_stations']
    else:
        treads = len(params['sta_where_packets_arrive'])
    size = params['num_generated_packets'] * params['num_stations'] * treads

    return get_random_eval(average, std, size)
