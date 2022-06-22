# bill.py
# JM Kinser
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np

# read the data
def Read( fname ):
    a = open( fname ).read()
    a = a.lower()
    return a

# make a list of words
def MakeDict( instr, WL=1, retprobs=True ):
    # N is the word length
    L = len( instr )
    dct = {}
    for i in range( L-WL ):
        keyl = instr[i:i+WL]
        retral = instr[i+WL]
        if keyl in dct:
            if retral in dct[keyl][0]:
                ndx = dct[keyl][0].index( retral )
                dct[keyl][1][ndx] +=1
            else:
                dct[keyl][0].append( retral )
                dct[keyl][1].append( 1 )
        else:
            dct[keyl] = [[retral],[1]]
    K = list(dct.keys())
    if retprobs:  # if you want to returb probabilities
        for i in K:
            vec = np.array( dct[i][1] )
            vec = vec/vec.sum()
            dct[i][1] = vec
    return dct

def BuildString( dct, L, abet, WL ):
    # L is length of the output string
    # WL is word length in the dictionary
    # pick a starting string from the dictionary
    keys = list(dct.keys())
    stng = np.random.choice(keys)
    # build on this string
    for i in range( L ):
        preced = stng[-WL:] 
        if preced in dct:
            newlett = np.random.choice(dct[preced][0], p=dct[preced][1])
            stng += newlett
        else:
            r = int( np.random.ranf()*len(abet) )
            stng += abet[r]
    return stng



    
# a = Read( )
# WL = 7
# dct = shakespeare.MakeDict(sonnets,WL)
# output = shakespeare.BuildString(dct, 100, 'abcdefgh', WL)
# print(output)



