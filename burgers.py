import numpy as np
import matplotlib.pyplot as plt

def line_eqn(f, x_0, x):
    '''Characteristic equation in (x, t)-space, with slope = 1 / f(x_0).'''
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
    t_inter = line_eqn(f, x_1, x_inter)
    if t_inter is None:
        t_inter = line_eqn(f, x_2, x_inter)
    return [x_inter, t_inter]    


def fwd_propagate(f, x_space, t):
    '''Moves f(x_space) along characteristic lines until time t'''
    u_0 = f(x_space)
    new_x_space = np.zeros(len(x_space))
    for i in range(len(x_space)):
        x_i = x_space[i]
        new_x_space[i] = t * f(x_i) + x_i
    return new_x_space


def burgers(f, left = -2, right = 2, t_max = 4, numLines = 40, plotShockSol = True):
    '''
    Initial Condition: f(x) = u(x, 0)
    Plots characteristic equations for solutions to the Inviscid Burgers' equation.
    Resolves interceptions and interpolates possible discontinuities if they arise. 
    '''
    x_space = np.linspace(left, right, 1000)
    if plotShockSol:
        fig, (ax1, ax2, ax3) = plt.subplots(3, constrained_layout = True)
        fig.set_size_inches(6, 6)
    else: 
        fig, (ax1, ax2) = plt.subplots(2, constrained_layout = True)
        fig.set_size_inches(6, 9)

    ax1.set_title("Initial Condition (t = 0)")
    ax1.set_xlabel("x", weight = 'bold')
    ax1.set_ylabel("u(x, 0)", weight = 'bold')
    ax1.set_xlim([left, right])
    ax1.plot(x_space, f(x_space), 'b')

    ax2.set_title("Characteristic Lines in Space-Time")
    ax2.set_xlabel("x", weight = 'bold')
    ax2.set_ylabel("t", weight = 'bold')
    ax2.set_xlim([left, right])
    ax2.set_ylim([0, t_max])

    x_lines = np.linspace(left, right, numLines)

    collisions = []
    for i in range(numLines):
        x_0 = x_lines[i]
        for x_j in x_lines[i+1:]:
            collision = intersection(f, x_0, x_j)
            if collision:
                collisions.append([x_0, x_j] + collision)

    collisions.sort(key = lambda _: _[3])   #sort by time of collision  
    seen = []
    shocks = []
    while collisions: 
        [x_1, x_2, x_shock, t_shock] = collisions[0]
        if x_1 not in seen and x_2 not in seen:
            shocks.append([x_shock, t_shock])
            ax2.plot(x_shock, t_shock, 'r+', zorder = 2)

            #plot first characteristic from (x_1, 0) to (x_shock, t_shock)
            if f(x_1) == 0:
                ax2.axvline(x_1, ymax = t_shock / t_max, zorder = 1)
            else:
                if x_1 < x_shock:
                    x_smooth = np.linspace(x_1, x_shock)
                else:
                    x_smooth = np.linspace(x_shock, x_1)
                t_smooth = line_eqn(f, x_1, x_smooth)
                ax2.plot(x_smooth, t_smooth, 'tab:blue', zorder = 1)

            #plot second characteristic from (x_2, 0) to (x_shock, t_shock)
            if f(x_2) == 0:
                ax2.axvline(x_2, ymax = t_shock / t_max, zorder = 1)
            else:
                if x_2 < x_shock:
                    x_smooth = np.linspace(x_2, x_shock)
                else:
                    x_smooth = np.linspace(x_shock, x_2)
                t_smooth = line_eqn(f, x_2, x_smooth)
                ax2.plot(x_smooth, t_smooth, 'tab:blue', zorder = 1)
            seen.extend([x_1, x_2])
        collisions = collisions[1:]

    for x_0 in x_lines:
        if x_0 not in seen:
            if f(x_0) == 0:
                ax2.axvline(x_0, zorder = 1)
            else:
                t = line_eqn(f, x_0, x_space)
                ax2.plot(x_space, t, 'tab:blue', zorder = 1)
    
    if len(shocks) > 1:
        t_shock = shocks[0][1]
        print("t_shock = " + str(t_shock))

        #shock-front interpolation
        shocks.sort(key = lambda _: _[0])
        shocks = np.asarray(shocks)
        shock_x_space = np.linspace(shocks[0][0], shocks[-1][0])
        ax2.plot(shock_x_space, np.interp(shock_x_space, shocks[:, 0], shocks[:, 1]), color = 'red')
    
        #forward propagate initial condition until first shock
        if plotShockSol:
            x_space_t = fwd_propagate(f, x_space, t_shock)
            ax3.set_title("Shock Discontinuity (t = " + str(round(t_shock, 2)) + ")")
            ax3.set_xlabel("x", weight = 'bold')
            ax3.set_ylabel("u(x, t)", weight = 'bold')
            ax3.set_xlim([left, right])
            ax3.plot(x_space_t, f(x_space), 'red')
    #todo: animation
    plt.show()
    
'''
Initial Conditions u(x, 0) = f(x).
'''
def gaussian(x):
    return np.exp(-x**2)

def hyper(x):
    return np.tanh(-x)

'''Evans 3.4'''
def f_1(x):
    '''Shock Wave'''
    return np.piecewise(x, [x <= 0, x > 0, x > 1], [1, lambda x: 1-x, 0])

def f_2(x):
    '''Rarefaction Wave'''
    return np.piecewise(x, [x <= 0, x > 0], [0, 1])
    
def f_3(x):
    '''Shock + Rarefaction'''
    return np.piecewise(x, [x < 0, x >= 0, x > 1], [0, 1, 0])

#burgers(gaussian, plotShockSol = True)