import random
from itertools import count


def fatigue_param(microlapses: int, time: float, fp_dcc=0.98):
    """
    calculates and returns the fatigue module's modulation value (eq. 2)

    :param time: microlapses count >= 0
    :type time: int
    :param time: time in minutes
    :type time: float
    :param fp_dcc: degradation value
    :type fp_dcc: float
    """

    fp_pct = fp_dcc ** microlapses  # eq. 3
    return fp_pct * (1.0 + time) ** random.uniform(-1, 0)


def utility(microlapses, time, ui_t=5, noise_sigma=0.2):
    """
    calculates and returns the fatigue module's modulation value (eq. 1)

    :param time: microlapses count >= 0
    :type time: int
    :param time: time [0.0, 1.0]
    :type time: float
    :param ui_t: initial utility at time
    :type ui_t: float
    :param noise_sigma: noise sigma for randomly generated noise
    :type noise_sigma: float
    """

    fp_t = fatigue_param(microlapses, time)
    return fp_t * ui_t + random.normalvariate(0, noise_sigma)


def fatigue_thresh(time: float, ut_tot=-0.16):
    """
    calculates and returns the fatigue module's modulation value (eq. 5)

    :param time: time [0.0, 1.0]
    :type time: float
    :param ut_tot: utility threshold time-on-task decline parameter [-1.0, 0.0]
    :type ut_tot: float
    """

    return (1.0 + time) ** ut_tot


def utility_threshold(microlapses, time, ut_0=3.6, ut_tot=-0.16):
    """
    calculates and returns the utility threshold (used to represent increased effort)
    as compensation for feeling tired (eq. 4)

    :param time: microlapses count >= 0
    :type time: int
    :param time: time [0.0, 1.0]
    :type time: float
    :param ut_0: initial utility threshold intended to capture motivational factors
    :type ut_0: float
    :param ut_tot: utility threshold time-on-task decline parameter [-1.0, 0.0]
    :type ut_tot: float
    """

    ft_t = fatigue_thresh(time, ut_tot)
    return ft_t * ut_0


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    microlapses = 0
    x = np.linspace(0, 60, 1000)
    y = np.zeros(1000)
    z = np.zeros(1000)
    err = np.zeros(1000)
    for i, t in enumerate(x):
        microlapses += random.uniform(0, 1) > 0.98
        y[i] = utility(microlapses, t)
        z[i] = utility_threshold(microlapses, t, ut_0=4, ut_tot=-0.8)
        err[i] = y[i] < z[i]

    plt.plot(x, y, label='utility(t)')
    plt.plot(x, z, label='utility_threshold(t)')
    plt.xlabel('time')
    plt.legend()
    plt.savefig('validation_plots/utility.png')
    plt.show()

    plt.hist(y)
    plt.title('hist(utility(t))')
    plt.savefig('validation_plots/hist(utility(t)).png')
    plt.show()

    plt.plot(x, np.cumsum(err))
    plt.title('cumulative errors over time')
    plt.xlabel('time')
    plt.savefig('validation_plots/cumulative_errors.png')
    plt.show()

