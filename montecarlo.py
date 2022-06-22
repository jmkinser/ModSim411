# montecarlo.py
# JM Kinser
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np

def PIbyDarts( NumDarts, DM=2 ):
    vecs = 2 * np.random.ranf((NumDarts,DM)) - 1
    dists = np.sqrt((vecs**2).sum(1))
    NdartsIn = (dists < 1 ).sum()
    answer = 4.0 * NdartsIn / NumDarts
    return answer
