# star2.py
# JM Kinser
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import random
#%%

def SideOfLine( x,y, m, b):
    # is point (x,y) on near side or far side on line (m,b)
    if m==0:
        if y > b:
            return 'F'
        else:
            return 'N'
    else:
        mp = -1/m  # slope of intercept
        xp = -b/(m-mp)  #intersection
        yp = mp * xp
        #print(xp,yp)
        k = xp*xp + yp*yp # dot product
        k2 = xp*x + yp*y
        if k2>k:
            return 'F'
        else:
            return 'N'
#%%
def GetCode(x,y):
    answ = []
    answ.append( SideOfLine(x,y, 0,.112) ) # line 1
    answ.append( SideOfLine(x,y,.727,-.251)) # line 2
    answ.append( SideOfLine(x,y,-.72,-.251)) # line 3
    answ.append( SideOfLine(x,y,3.077,.476)) # line 4
    answ.append( SideOfLine(x,y,-3.077,.476)) # line 5
    # convert list to string
    answ = ''.join(answ)
    return answ
#%%
# check code
def IsInsideStar(x,y):
    incodes = ['FNNNN','NFNNN','NNFNN','NNNFN', 'NNNNF', 'NNNNN']
    c = GetCode( x,y )
    if c in incodes:
        return True
    else:
        return False
#%%
def RandomPoint( ):
    x = 1*random.random() - 0.5
    y = .951*random.random() - .475
    return (x,y)    
#%%
# test
def Test():
    xmin, xmax, ymin, ymax = 0,0,0,0
    for i in range( 1000000):
        x,y = RandomPoint()
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    print( xmin, xmax, ymin, ymax )
#%%
def ManyRandomPoints( Nvectors ):
    ct = 0
    for i in range( Nvectors ):
        x,y = RandomPoint()
        if IsInsideStar( x,y ):
            ct += 1
    return ct/Nvectors
#%%
import numpy as np
import scipy.misc as sm

def TestStarImage(Ndarts):
    answ= np.zeros((951,1000,3))
    for i in range( Ndarts ):
        x,y = RandomPoint()
        xx = int((.5+x)*1000)
        yy = int((.475+y)*1000)
        if IsInsideStar(x,y)==True:
            answ[yy,xx,1] = 255
        else:
            answ[yy,xx,0] = 255
    sm.imsave('dud.png', answ)
#TestStarImage(1000000)