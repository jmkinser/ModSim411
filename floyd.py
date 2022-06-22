# floyd.py
# Floyd-Warshall
# JM Kinser
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np

# faster in Python but I have not put in the p-matrix
def FastFloyd( w ):
    d = w + 0
    N = len( d )
    oldd = d + 0
    for k in range( N ):
        if k%50==0: print(k,end=' ')
        newd = np.add.outer( oldd[:,k], oldd[k] )
        #m = greater( newd, 700 )
        #newd = (1-m)*newd + m * oldd
        mask = newd < oldd
        mmask = 1-mask
        g = mask*newd + mmask * oldd
        oldd = g + 0
    return g

# faster in Python
def FastFloydP( ing, inp ):
    # ing is the distances
    # inp is the connections  cnnxs*indices[0] 
    d = ing + 0
    N = len( d )
    oldd = d + 0
    p = inp + 0
    for k in range( N ):
        if k%50==0: print (k,end=' ')
        newd = np.add.outer( oldd[:,k], oldd[k] )
        #m = greater( newd, 700 )
        #newd = (1-m)*newd + m * oldd
        mask = np.less( newd, oldd )
        mmask = 1-mask
        g = mask*newd + mmask * oldd
        oldd = g + 0
        p = (1-mask)*p + mask * p[k]
        #print mask1, '\n',mask
        #print(g)
        #print(p)
    return g, p

# find a path
def FindPath( P, K, L ):
    # P from FastFloydP
    # K L are the start and end points
    pth = [ L ]
    n = P[K,L]
    while n != K:
        pth.append( int(n) )
        n = int(P[K,n])
    pth.append( K )
    pth.reverse()
    return pth
    
    
