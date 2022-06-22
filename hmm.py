# hmm2.py
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np

# hardcode a system
def TrialSystem():
    # emission HMM.  Each node has an emission dictionary, 
    # and a transition integer.  The HMM is a dictionary of
    # these nodes
    hmm = {}
    hmm[0] = ({'A':0.3, 'B':0.2, 'C':0.5 }  , 1 )
    hmm[1] = ({ 'A':0.1, 'B':0.8, 'C':0.1} , 2) 
    hmm[2] = ({ 'A':0.4, 'B':0.6} , -1 ) 
    return hmm


# Emission HMM Recall
def ERecall( hmm, strng ):
    # strng is the input data string
    prb = 1 # initialization
    N = len( strng )
    for i in range( N ):
        if strng[i] in hmm[i][0]:
            prb *= hmm[i][0][ strng[i] ]
        else:
            prb = 0
            break
    return prb
    
def SimpleTHMM( ):
    net = {}
    net['begin'] = ('',{0:1.0} )
    net[0] = ('A', {1:0.3,2:0.7} )
    net[1] = ('B', {3:1.0} )
    net[2] = ('C', {3:1.0} )
    net[3] = ('D', {'end':1.0} )
    net['end'] = ('',{} )
    return net

def NextNode( net, k, ask ):
    t = net[k][1].keys() # transition for this node
    hit = []
    for i in t:
        if net[i][0]==ask:
            hit = i, net[k][1][i]
            break
    return hit

def TProb( net, instr ):
    L = len( instr )
    pbs = 1.0
    k = 'begin'
    for i in range( L ):
        tran = NextNode( net,k,instr[i])
        k = tran[0]
        pbs *= tran[1]
    return pbs

def NodeTable( sts, abet):
    # sts is a list of data strings
    L = len( sts )  # the number of strings
    D = len( sts[0] )   # length of string
    A = len( abet )
    NT = np.zeros( (A,D),int )-1
    nodecnt = 0
    for i in range( D ):
        for j in range( L ):
            ndx = abet.index( sts[j][i] )
            if NT[ndx,i] ==-1:
                NT[ndx,i] = nodecnt
                nodecnt +=1
    return NT

def MakeNodes( sts, abet, weights, nodet ):
    L = len( sts )
    D = len( sts[0] )   # length of string
    net = {}
    for j in range( D-1):
        for i in range( L ):
            # current letter
            clet = sts[i][j]
            # next letter
            nlet = sts[i][j+1]
            # node associated with current letter
            cnode = nodet[ abet.index(clet), j ]
            # node associated with next letter
            nnode = nodet[ abet.index(nlet), j+1]
            # connect the nodes
            if cnode in net:
                # transition has been seen before
                # adjust the transition
                if nnode in net[cnode][1]:
                    net[cnode][1][nnode] += weights[i]
                else:
                    net[cnode][1][nnode] = weights[i]
            else:
                # transition has not been seen before - make new one
                net[cnode]= ( clet ,{ nnode: weights[i] })
    return net


def Normalization( net ):
    t = net.keys()
    for i in t:
        sm = 0
        for j in net[i][1].keys():
            sm += net[i][1][j]
        for j in net[i][1].keys():
            net[i][1][j] /= sm

def Ends( net, sts, abet, weights, nodet ):
    # add begin node
    T = {}
    L = len( sts )
    for i in range(L):
        clet = sts[i][0] # first letter in string i
        nlet = sts[i][1]
        idt = nodet[ abet.index(clet) ,0]
        # Build dictionary for the BEGIN node
        if idt != -1:
            if idt in T:
                T[ idt] += weights[i]
            else:
                T[ idt] = weights[i]
    net['begin'] = ( '', T )
    # add end node
    net['end'] = ('',{} )
    for i in range( L ):
        clet = sts[i][-1]
        idt = nodet[ abet.index(clet) ,-1]
        net[idt] = (clet,{'end':1})

