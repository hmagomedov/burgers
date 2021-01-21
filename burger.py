import numpy as np
import matplotlib.pyplot as plt


def gaussian(x):
    #initial condition u(x, 0) = f(x)
    return np.exp(-x**2)


def f(x):
    return np.piecewise(x, [x < 0, x >= 0], [1, 0])


def lineEqn(f, x_0, x):
    '''Slope = 1 / f(x_0).'''
    if f(x_0) == 0:
        return None
    return (x - x_0)/f(x_0)


def intersection(f, x_1, x_2):
    '''Returns (x, t)-coordinates of intersection between two characteristic lines.'''
    if x_1 > x_2:
        #ensure x_1 < x_2
        x_1, x_2 = x_2, x_1
    if f(x_1) <= f(x_2):
        return None
    x_inter = (x_2 * f(x_1) - x_1 * f(x_2)) / (f(x_1) - f(x_2))
    t_inter = lineEqn(f, x_1, x_inter)
    if t_inter is None:
        t_inter = lineEqn(f, x_2, x_inter)
    return [x_inter, t_inter]


def main(f, left, right):
    x_space = np.linspace(left, right)
    fig, (ax1, ax2) = plt.subplots(2, constrained_layout = True)

    ax1.set_title("Initial Condition (t = 0)")
    ax1.set_xlabel("x", weight = 'bold')
    ax1.set_ylabel("u(x, 0)", weight = 'bold')
    ax1.set_xlim([left, right])
    ax1.plot(x_space, f(x_space), 'b')

    ax2.set_title("Characteristic Lines in Space-Time")
    ax2.set_xlabel("x", weight = 'bold')
    ax2.set_ylabel("t", weight = 'bold')
    ax2.set_xlim([left, right])
    ax2.set_ylim([0, right-left])

    num_lines = 21
    x_lines = np.linspace(left, right, num_lines)

    collisions = []
    for i in range(num_lines):
        x_0 = x_lines[i]
        for x_j in x_lines[i+1:]:
            collision = intersection(f, x_0, x_j)
            if collision:
                collisions.append([x_0, x_j] + collision)

    collisions.sort(key = lambda _: _[3])   #sort by time of collision  
    seen = []
    while collisions: 
        [x_1, x_2, x_shock, t_shock] = collisions[0]
        if x_1 not in seen and x_2 not in seen:
            ax2.plot(x_shock, t_shock, 'r+', zorder = 2)
            
            #plot first characteristic from (x_1, 0) to (x_shock, t_shock)
            if f(x_1) == 0:
                ax2.axvline(x_1, ymax = t_shock / (right-left), zorder = 1)
            else:
                if x_1 < x_shock:
                    x_smooth = np.linspace(x_1, x_shock)
                else:
                    x_smooth = np.linspace(x_shock, x_1)
                t_smooth = lineEqn(f, x_1, x_smooth)
                ax2.plot(x_smooth, t_smooth, 'tab:blue', zorder = 1)

            #plot second characteristic from (x_2, 0) to (x_shock, t_shock)
            if f(x_2) == 0:
                ax2.axvline(x_2, ymax = t_shock / (right-left), zorder = 1)
            else:
                if x_2 < x_shock:
                    x_smooth = np.linspace(x_2, x_shock)
                else:
                    x_smooth = np.linspace(x_shock, x_2)
                t_smooth = lineEqn(f, x_2, x_smooth)
                ax2.plot(x_smooth, t_smooth, 'tab:blue', zorder = 1)
            seen.extend([x_1, x_2])
        collisions = collisions[1:]

    for x_0 in x_lines:
        if x_0 not in seen:
            if f(x_0) == 0:
                ax2.axvline(x_0, zorder = 1)
            else:
                t = lineEqn(f, x_0, x_space)
                ax2.plot(x_space, t, 'tab:blue', zorder = 1)
    
main(f, -2, 2)
plt.show()
main(gaussian, -2, 2)
plt.show()