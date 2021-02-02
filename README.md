# Shock Discontinuities for Inviscid Burgers' Equation

A visualization of the method of characteristics for the Inviscid Burgers' equation: 

`u_t + u * u_x = 0`

For any initial condition `f(x) = u(x, 0)`, simply call `burgers(f)`.  The characteristic lines are plotted, and any collisions between them are shown. A characteristic line represents a set in space-time where a solution `u(x, t)` is constant. If any characteristics intersect, a discontinuity in the solution occurs and the program interpolates a shock-front in space-time.

If `plotShockSol = True`, the initial state `f(x)` is moved forward in time along non-intersecting characteristics until the first collision is detected. This represents the last continuous solution prior to the onset of the shock discontinuity. The time of shock becomes more accurate as more characteristic lines are plotted.

`f` must accept array inputs. Specify the (x, t)-domain and other parameters as follows:

``burgers(f, left, right, t_max, numLines = 40, plotShockSol = True)``

The following example taken from Evans PDE 3.4 illustrates both a rarefaction and a shockwave. There are characteristics which intersect immediately at t = 0, so we leave `plotShockSol = False`.

```
def f_3(x):
    '''Shock + Rarefaction'''
    return np.piecewise(x, [x < 0, x >= 0, x > 1], [0, 1, 0])
    
burgers(f_3, plotShockSol = False)
```
<img src="https://github.com/hmagomedov/burgers/blob/main/Evans_3.png"/>


This second example illustrates the shock that occurs with a Gaussian initial condition. The discontinuity in the solution is apparent as it is on the verge of becoming multi-valued.

```
def gaussian(x):
    return np.exp(-x**2)

burgers(gaussian, -3, 3, 10)
```
<img src="https://github.com/hmagomedov/burgers/blob/main/Gaussian.png"/>

