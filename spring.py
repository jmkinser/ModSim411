# spring.py
# JM Kinser
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.



# spring.py
def Spring():
    k = 0.5 # spring constant
    x = 0.5 # initial stretch
    m = 1 # mass
    v1 = 0 # initial velocity
    dt = 0.1 # time step
    x1 = x
    for i in range( 200 ):
        a = -k * x1 / m
        v2 = v1 + a * dt
        x2 = x1 + v1 * dt + 0.5 * a * dt * dt
        v1 = v2
        x1 = x2
        print( i, x2 )
#%%
def Spring2(niter=200):
    xx = []
    k = 0.5 # spring constant
    x = 0.5 # initial stretch
    m = 1 # mass
    v1 = 0 # initial velocity
    dt = 0.1 # time step
    x1 = x
    for i in range( niter ):
        a1 = -k * x1 / m
        v2 = v1 + a1 * dt
        x2 = x1 + v1 * dt + 0.5 * a1 * dt * dt
        a2 = -k * x2/m
        a = (a1+a2)/2
        v2 = v1 + a *dt
        x2 = x1 + v1 * dt + 0.5 * a * dt * dt
        v1 = v2
        x1 = x2
        xx.append(x2)
    return xx
#%%
# leapfrog
def Leapfrog(niter=200):
    xx = []
    k = 0.5 # spring constant
    x = 0.5 # initial stretch
    m = 1 # mass
    v1 = 0 # initial velocity
    dt = 0.1 # time step
    x1 = x
    for i in range( niter ):
        a2 = -k * x1 / m
        v2 = v1 + a2 * 0.5*dt
        x2 = x1 + v1 * dt + 0.5 * a2 * dt * dt
        v1 = v2
        x1 = x2
        xx.append(x2)
    return xx
#%%
#xx = Leapfrog(100000)
#plt.plot(xx)
#plot.show()
