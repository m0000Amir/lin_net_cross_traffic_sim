import numpy as np


from queue_model.randoms import get_random_eval


def get_arrival_times(params: dict) -> np.ndarray:
    """
    Prepare random variables of arrival packet times
    Parameters
    ----------
    params: input parameters

    Returns
    -------
        Vector of arrival packet times
    """
    average = params['mean_arrival_time']
    std = params['std_arrival_time']
    size = params['num_generated_packets']

    return get_random_eval(average, std, size)


def get_arrival_packet_receivers(params: dict) -> np.ndarray:
    """
    Prepare random variables of arrival packet receivers

    Parameters
    ----------
    params: dict

    Returns
    -------
        Vector of arrival packet receivers

    """
    if params['mode'] == 'UPLOAD':
        receivers = np.ones(params['num_generated_packets']) * (
                params['num_stations'] - 1)
        return receivers.astype(int)
    elif params['mode'] == 'UPLOADDOWNLOAD':
        return np.random.choice(params['num_stations'],
                                params['num_generated_packets'])
