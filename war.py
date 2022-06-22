# war.py
# JM Kinser
# September 2020
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np
import random
import matplotlib.pyplot as plt
#%%
## Create Deck, shuffle distribute, pilebins, cardcount
def Start():
    # create deck
    deck = list(range(2,15)) * 4
    np.random.shuffle(deck) # shuffle deck
    # deal
    p1 = deck[:26]
    p2 = deck[26:]
    # create other 
    p1count = [26]
    pile1=[]; pile2=[]
    return p1, p2, p1count, pile1, pile2


def Play1(p1, p2, p1count, pile1, pile2):
    # pick cards at random
    #print('play',p1,p2, pile1, pile2)
    pile1.append( p1.pop(0) )
    pile2.append( p2.pop(0) )
    # Compare
    if pile1[-1]==pile2[-1]:
        #print('tie')
        if len(p1)==0:
            WinRound(p2,pile2,pile1)
        if len(p2)==0:
            WinRound(p1,pile1,pile2)
        Tie(p1, p2, p1count, pile1, pile2)
    elif pile1[-1]>pile2[-1]:
        WinRound(p1,pile1,pile2)
    elif pile1[-1]<pile2[-1]:
        WinRound(p2,pile2,pile1)
    p1count.append( len(p1))
    if len(p1)<1 or len(p2)<1:
        return False
    else:
        return True
    
def WinRound(pwin,pilewin,pilelose):
    pwin.extend(pilewin)
    pwin.extend(pilelose)
    pilewin.clear()
    pilelose.clear()
        
def Tie(p1,p2,p1count, pile1, pile2):
    # player 1
    # number of cards to play face down.
    if len(p2)>1:
        N = min((3,len(p2)-1))
        for i in range(N):
            pile2.append(p2.pop(0))
    if len(p1)>1:
        N = min((3,len(p1)-1))
        for i in range(N):
            pile1.append(p1.pop(0))
        
def RunGame(p1, p2, p1count, pile1, pile2):
    ok = True
    rounds= 0
    while ok:
        ok = Play1(p1, p2, p1count, pile1, pile2)
        rounds += 1
    if len(p1)>1:
        return 1, rounds
    else:
        return 2, rounds
#%%
def Go(N=1000):
    ct = 0
    wrounds = []
    for i in range(N):
        p1, p2, p1count, pile1, pile2 = Start()
        win, rounds = RunGame(p1, p2, p1count, pile1, pile2)
        ct += win
        if win==1:
            wrounds.append( rounds )
    wrounds = np.array( wrounds )
    return ct, wrounds
#%%
# Test.  Player 1 starts with 1 ace
def Start2():
    # create deck
    deck = list(range(2,15)) * 4
    # shuffle deck
    np.random.shuffle( deck )
    # deal
    p1 = [14]
    deck.remove(14)
    p2 = deck
    # create other 
    p1count = [1]
    pile1=[]; pile2=[]
    return p1, p2, p1count, pile1, pile2

def Go2(N=1000):
    ct = 0
    wrounds = []
    for i in range(N):
        p1, p2, p1count, pile1, pile2 = Start2()
        win, rounds = RunGame(p1, p2, p1count, pile1, pile2)
        ct += win
        if win:
            wrounds.append( rounds )
    wrounds = np.array( wrounds )
    return ct, wrounds
    
#%%
# player 1 starts with 4 aces.
def Start3():
    # create deck
    deck = list(range(2,15)) * 4
    # shuffle deck
    np.random.shuffle( deck )
    # deal
    p1 = [14,14,14,14]
    for i in range( 4):
        deck.remove(14)
    p2 = deck
    # create other 
    p1count = [1]
    pile1=[]; pile2=[]
    return p1, p2, p1count, pile1, pile2

def Go3(N=1000):
    ct = 0
    wrounds = []
    for i in range(N):
        p1, p2, p1count, pile1, pile2 = Start3()
        #print(p1)
        win,rounds = RunGame(p1, p2, p1count, pile1, pile2)
        ct += win
        if ct:
            wrounds.append(rounds)
    print(ct,N)
    wrounds = np.array(wrounds)
    return ct, wrounds
#%%
