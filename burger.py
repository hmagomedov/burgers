import numpy as np
import matplotlib.pyplot as plt


def gaussian(x):
    #initial condition u(x, 0) = f(x)
    return np.exp(-x**2)


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
    step = (right - left) / num_lines
    print("stepsize = " + str(step))
    
    x_0 = left
    while x_0 < right:
        if f(x_0) == 0:
            ax2.axvline(x_0)
        else:
            ax2.plot(x, (x-x_0)/f(x_0), 'b', label = 'r')
        x_0 += step
    
main(gaussian, -2, 2)
plt.show()

