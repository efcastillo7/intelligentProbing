from matplotlib import pyplot as mp
import numpy as np

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

for mu, sig in [(0, 2)]:
    mp.plot(gaussian(np.linspace(-3, 3, 120), mu, sig))

    print(gaussian(np.linspace(-3, 3, 120), mu, sig))

mp.show()