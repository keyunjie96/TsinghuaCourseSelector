import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

for i in range(16, 256, 16):
    infile = open(str(i) + ".txt")
    result = list()
    for each in infile:
        result.append(int(each.strip("\n")))
    plt.hist(result, bins=max(result) - min(result))
    plt.savefig(str(i)+".jpg")
    plt.close()
