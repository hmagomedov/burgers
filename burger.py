import numpy as np
import matplotlib.pyplot as plt


def gaussian(x):
    #initial condition u(x, 0) = f(x)
    return np.exp(-x**2)

def f(x):
    return np.piecewise(x, [x < 0, x >= 0], [1, 0])

def intersection(f, x_1, x_2):
    '''Returns x-coordinate of intersection between two characteristic lines, with slope = 1 / f(x).'''
    if f(x_1) == f(x_2):
        return None
    if (x_1 < x_2 and f(x_1) < f(x_2)) or (x_1 > x_2 and f(x_1) > f(x_2)):
        return None
    return (x_1 - f(x_1)*(x_2)) / (f(x_2) - f(x_1))

def main(f, left, right):
    x = np.linspace(left, right)

    fig, (ax1, ax2) = plt.subplots(2, constrained_layout = True)
    ax1.set_title("Initial Condition (t = 0)")
    ax1.set_xlabel("x", weight = 'bold')
    ax1.set_ylabel("u(x, 0)", weight = 'bold')
    ax1.set_xlim([left, right])


    ax2.set_title("Characteristic Lines in Space-Time")
    ax2.set_xlabel("x", weight = 'bold')
    ax2.set_ylabel("t", weight = 'bold')
    ax2.set_xlim([left, right])
    ax2.set_ylim([0, right-left])


    ax1.plot(x, f(x))

    num_lines = 20
    x_lines = np.linspace(left, right, num_lines)
    
    for x_0 in x_lines:
        if f(x_0) == 0:
            ax2.axvline(x_0)
        else:
            ax2.plot(x, (x-x_0)/f(x_0), 'b', label = 'r')
    
#main(f, -2, 2)
#plt.show()

print(intersection(f, -1, 1))
