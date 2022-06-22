# schelling.py
# JM Kinser
# September 2020
# (C) Jason Kinser.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np
import scipy.ndimage.interpolation as ndi
import imageio

#%%
def Init(V,H,pctempty):
    #global grid
    grid=np.zeros((V,H),int)
    # populate
    t1 = pctempty # first threshold
    t2 = (1-t1)/2 + t1 # second threshold
    r = np.random.rand(V,H)
    mask1 = (r>t1)*(r<=t2)
    mask2 = (r>t2)
    grid = grid + mask1 + mask2*2
    return grid
#%%	
def Init2(V,H,pctempty):
    grid=np.zeros((V,H),int)
    # populate
    t1 = pctempty # first threshold
    t2 = (1-t1)/2 + t1 # second threshold
    r = np.random.rand(V,H)
    mask1 = (r>t1)*(r<=t2)
    mask2 = (r>t2)
    grid = grid + mask1 + mask2*2
    return grid


def Init4(V,H,pctempty):
    global grid
    grid=np.zeros((V,H),int)
    # populate
    t1 = pctempty # first threshold
    step = (1-t1)/4
    t2 = t1+step
    t3 = t2 + step
    t4 = t3 + step
    r = np.random.rand(V,H)
    mask1 = (r>t1)*(r<=t2)
    mask2 = (r>t2)*(r<=t3)
    mask3 = (r>t3)*(r<=t4)
    mask4 = (r>t4)
    print(step,t1,t2,t3,t4)
    grid = grid + mask1 + mask2*2 + mask3*3 + mask4*4

#%%
def Unhappy( grid ):
    unhappy = np.zeros( grid.shape, int )
    shifts = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
    for sh in shifts:
        alt = ndi.shift(grid, sh )
        temp = grid != alt
        unhappy +=  temp * (alt!=0)
    unhappy *= (grid!=0)
    return unhappy
#%%    

def CollectGrumps(uhap, gamma=5):
    mask = uhap>=gamma
    v,h = mask.nonzero()
    return v,h
    
def FindEmpty(grid):
    ev,eh = (grid==0).nonzero()
    return ev,eh

# original (that worked)
def Move1Unhappy(v,h,ev,eh,grid):
    N = len(v)
    if N>0:
        me = np.random.randint(0,N)
        mover = v[me],h[me]
        M = len(ev)
        me = np.random.randint(0,M)
        newloc = ev[me],eh[me]
        # move
        oldg = grid[newloc]
        grid[newloc] = grid[mover]
        grid[mover] = oldg
        
#
    
def Iterate(grid, gamma=4):
    u = Unhappy(grid)
    v,h = CollectGrumps(u,gamma)
    ev,eh = FindEmpty(grid)
    Move1Unhappy(v,h,ev,eh,grid)
#%%
# imageio.imsave('dud.png',grid.astype(np.uint8))
def Go():
    grid = Init(100,100,0.008)
    for i in range( 25 ):
        for j in range( 2500 ):
            Iterate(grid)
        u = Unhappy(grid)
        print((u>=4).sum())
        imageio.imsave('dud'+str(i) + '.png',(100*grid).astype(np.uint8))
        if (u>=4).sum() == 0:
            break

#%%

# four animals
def Go4():
    Init4(100,100,0.01)
    for i in range( 10 ):
        for j in range( 500000 ):
            Iterate(grid)
        u = Unhappy(grid)
        print((u>=4).sum())
        imageio.imsave('dud'+str(i) + '.png',(100*grid).astype(np.uint8))
        
# ###########  3D
def Init3D(V,H,N,pctempty):
    grid=np.zeros((V,H,N),int)
    # populate
    t1 = pctempty # first threshold
    t2 = (1-t1)/2 + t1 # second threshold
    r = np.random.rand(V,H,N)
    mask1 = (r>t1)*(r<=t2)
    mask2 = (r>t2)
    grid = grid + mask1 + mask2*2
    return grid

def Unhappy3D( grid ):
    unhappy = np.zeros( grid.shape, int )
    shifts = []
    for i in range(-1,2):
        for j in range(-1,2):
            for k in range(-1,2):
                shifts.apppend( (i,j,k))
    shifts.remove((0,0,0))
    for sh in shifts:
        alt = ndi.shift(grid, sh )
        temp = grid != alt
        unhappy +=  temp * (alt!=0)
    unhappy *= (grid!=0)
    return unhappy

def CollectGrumps3D(uhap, gamma=13):
    mask = uhap>=gamma
    v,h,w = mask.nonzero()
    return v,h,w
    
def FindEmpty3D(grid):
    ev,eh,ew = (grid==0).nonzero()
    return ev,eh,ew

def Move1Unhappy3D(v,h,w,ev,eh,ew,grid):
    N = len(v)
    M = len(ev)
    if N>1 and M>1:
        me = np.random.randint(0,N)
        mover = v[me],h[me],w[me]
        me = np.random.randint(0,M)
        newloc = ev[me],eh[me], ew[me]
        # move
        oldg = grid[newloc]
        grid[newloc] = grid[mover]
        grid[mover] = oldg

def Iterate3D(grid, gamma=13):
    u = Unhappy3D(grid)
    v,h,w = CollectGrumps3D(u,gamma)
    ev,eh,ew = FindEmpty3D(grid)
    Move1Unhappy3D(v,h,w,ev,eh,ew,grid)

def Go3D():
    grid = Init3D(100,100,50,0.008)
    for i in range( 25 ):
        for j in range( 10000 ):
            Iterate3D(grid)
    return grid
        #u = Unhappy3D(grid)
        #print((u>=4).sum())
        #imageio.imsave('dud'+str(i) + '.png',(100*grid[:,:,50]).astype(np.uint8))
