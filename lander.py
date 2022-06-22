# lander.py

import numpy as np
import matplotlib.pyplot as plt

#%%
## Initialize
def InitLander():
    y1 = 1000
    m1 = 15000
    g = -2
    v1 = 0
    time = 0.0
    dt = 0.1
    force = 50000
    k = 100
    return y1, v1, m1, g, time, dt, force, k

def Burn( time, m1, force, k, burns ):
    aplus = 0
    for t1, d in burns:
        if t1 < time < t1 + d:
            aplus = force/m1
            m1 = m1 - k
            break
    return aplus, m1

def Iterate(g, y1, v1, aplus, dt):
    accel = g + aplus
    v2 = v1 + accel * dt
    y2 = y1 + v1*dt + 0.5*accel * dt**2
    return y2, v2, accel
    
    
# burn = [ (10,2),(15,2), (20,3), (30,3), (35,3)]
def RunLander( initvals, burns ):
    y1, v1, m1, g, time, dt, force, k = initvals
    vs, ys, acs = [],[],[]
    ok = True
    while ok:
        aplus, m1 = Burn(time, m1, force, k, burns)
        y2, v2, accel = Iterate( g, y1, v1, aplus, dt )
        vs.append( v2 ); ys.append(y2), acs.append( accel)
        if m1 < 1000 or y2 <= 0:
            ok = False
        y1, v1 = y2, v2
        time += dt
    return ys, vs, acs

def PlotLander( ys, vs, acs ):
    ys1 = np.array( ys )/100.
    vs1 = np.array( vs )/5.
    plt.plot(np.zeros(len(ys1)))
    plt.plot(vs1)
    plt.plot(ys1)
    plt.plot(acs)
    plt.show()

def Test():
    initvals = InitLander()
    burns = [(4.98,0.37), (19.1,1.3),(26.1,2.45), (29.1,4.2), (34.3,3.5)]
    ys, vs, acs = RunLander( initvals, burns )
    Plot( ys, vs, acs)
    
def ManyTrials(N = 10, gamma = 5):
    goodburns = []
    for n in range( N ):
        burns = []
        for i in range( 5 ):
            a = 35 * np.random.random()
            b = 5 * np.random.random()
            burns.append( (a,b) )
        initvals = InitLander()
        ys, vs, acs = RunLander( initvals, burns )
        if abs(vs[-1]) < gamma:
            goodburns.append( burns )
    return goodburns