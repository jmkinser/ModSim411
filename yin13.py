# -*- coding: utf-8 -*-
"""
yin13.py
Version 1: JM Kinser May 2020
"""
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np
import matplotlib.pyplot as plt
#%%
def GatherData(sname,nname,pct):
    with open(sname) as f:
        data = f.read().splitlines()
    np.random.shuffle(data)
    N = int(pct*len(data))
    trainstarts = data[:N]
    notrainstarts = data[N:]
    with open(nname) as f:
        nonstarts = f.read().splitlines()      
    np.random.shuffle(nonstarts)
    return trainstarts, notrainstarts, nonstarts
#%%

def Build4Mat( stdata, K, abet='acgt' ):
    # K is first column number
    N = len( stdata )  # number of strings
    mat = np.zeros( (4,4) )
    for i in range( N ):
        k1 = abet.index( stdata[i][K] )
        k2 = abet.index( stdata[i][K+1] )
        mat[k1,k2] += 1
    # no zeros allowed
    mask = mat==0
    mat = mask*1 + (1-mask)*mat
    # probs
    for i in range( 4 ):
        mat[i] /= mat[i].sum()
    probs = mat + 0
    # log odds
    mat /= 0.25
    mat = np.log(mat )
    return probs, mat

## build HMM
def BuildHMM( stdata ):
    N = len( stdata[0] ) # length of a string
    probs = np.zeros( (N-1, 4,4 ) )
    logodds = np.zeros( (N-1, 4,4 ) )
    for i in range( N-1):
        probs[i], logodds[i] = Build4Mat( stdata, i )
    return probs, logodds

## run a query through the HMM
def SingleProbQuery( probs, query, abet='acgt' ):
    sc = 1
    N = len( probs ) # number of matrices
    for i in range( N ):
        k1 = abet.index( query[i] )
        k2 = abet.index( query[i+1] )
        sc *= probs[i][k1,k2]
    return sc

## run a query through the HMM
def SingleQuery( hmms, query, abet='acgt' ):
    sc = 0
    N = len( hmms ) # number of matrices
    for i in range( N ):
        k1 = abet.index( query[i] )
        k2 = abet.index( query[i+1] )
        sc += hmms[i][k1,k2]
    return sc

## run lots of queries
def ManyQueries( hmms, queries ):
    N = len( queries ) # number of queries
    answ = np.zeros( N )
    for i in range( N ):
        answ[i] = SingleQuery( hmms, queries[i] )
    return answ
#%%
def GatherData(sname,nname,pct):
    # fname = starts.txt
    # pct: percent of strings used in training
    ## load the start data
    with open(sname) as f:
        data = f.read().splitlines()
    ## randomize
    np.random.shuffle(data)
    ## Divide into train and nontrain
    N = int(pct*len(data))
    trainstarts = data[:N]
    notrainstarts = data[N:]
    with open(nname) as f:
        nonstarts = f.read().splitlines()      
    np.random.shuffle(nonstarts)
    return trainstarts, notrainstarts, nonstarts
    
#trainstarts, notrainstarts, nonstarts = GatherData('starts.txt', 'nonstarts.txt', 0.1)
#%%
# codes to run
# probs, logodds = BuildHMM(trainstarts)
# SingleQuery(logodds,trainstarts[0])
# scores = ManyQueries(logodds,trainstarts)
def TestHMM(data, logodds):
    # data = [trainstarts, notrainstarts, nonstarts]
    means, stds = [],[]
    for i in range(len(data)):
        print(i)
        scores = ManyQueries(logodds,data[i])
        means.append(scores.mean())
        stds.append(scores.std())
    return means, stds

#means,stds = TestHMM(data,logodds)
    
#%%
def Plot(means, stds):
    N = len(means)
    x = np.linspace(-2,12)
    for i in range(N):
        y = np.exp(-((x-means[i])**2)/(2*stds[i]**2))
        plt.plot(x,y)

#Plot(means,stds)    