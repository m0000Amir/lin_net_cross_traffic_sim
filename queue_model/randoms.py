"""
Get evaluation of random variables
Distributions are selected from the following:
    - Exponential distribution (cv = 1);
    - Erlang distribution (cv <= 1);
    - Hyperexponential distribution (cv >= 1),
where cv is Coefficient of variation.
"""
import numpy as np
import math


class Exponential:
    """
    Exponential distribution
    E(1/avg)
    """
    def __init__(self):
        self.rate = None

    def eval(self, average: float, size: int) -> np.ndarray:
        self.fit(average)
        return np.random.exponential(scale=1/self.rate, size=size)

    def fit(self, average: float) -> None:
        self.rate = 1 / average


class Erlang:
    """
    Erlang distribution
    E(1/avg, shape)
    """
    def __init__(self):
        self.rate = None
        self.shape = None

    def eval(self, average: float, std: float, size: int) -> np.ndarray:
        self.fit(average, std)
        return np.random.gamma(scale=1/self.rate, shape=self.shape, size=size)

    def fit(self, average: float, std: float) -> None:
        cv = std / average
        self.rate = average / std ** 2
        self.shape = int(np.round(average ** 2 / std ** 2))


class HyperExponential:
    """
    Hyperexponential distribution
    E(1/avg, probability)
    """
    def __init__(self):
        self.rate = None
        self.prob = None

    def eval(self, average: float, std: float, size: int) -> np.ndarray:
        self.fit(average, std)
        state_indexes = np.random.choice(len(self.prob), size, p=self.prob)
        values = [np.random.exponential(1/self.rate[si])
                  for si in state_indexes]
        return np.asarray(values)

    def fit(self, average: float, std: float) -> None:
        # TODO: CHECK FITTING VARIABLES
        cv = std / average
        prob1 = 0.5 * (1 + np.sqrt((cv ** 2 - 1)/ (cv ** 2 + 1)))
        prob2 = 1 - prob1
        rate1 = 2 * prob1 / average
        rate2 = 2 * (1 - prob1) / average
        self.rate = [rate1, rate2]
        self.prob = [prob1, prob2]


def get_random_eval(average: float, std: float, size: int) -> np.ndarray:
    cv = std / average
    if (cv == 1) or (math.isclose(std, average, rel_tol=0.1)):
        return Exponential().eval(average, size)
    elif cv <= 1:
        return Erlang().eval(average, std, size)
    else:
        return HyperExponential().eval(average, std, size)
