# -*- coding: utf-8 -*-
# sodoku.py
"""
Created on Wed Apr  6 14:46:11 2016
Modified 4.26.19
@author: jkinser
"""
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import numpy as np
#%%

def Architecture1():
    groups = []
    x = np.array((0,1,2,3,4,5,6,7,8))
    for i in range( 9 ):
        groups.append( list(x + i*9))
    for i in range(9):
        groups.append( list(x*9 + i) )
    x = np.array( (0,1,2,9,10,11,18,19,20))
    for i in (0,27,54):
        for j in (0,3,6):
            groups.append(list(x+i+j))
    return groups

def Architecture2():
    groups = []
    x = np.array((0,1,2,3,4,5,6,7,8))
    for i in range( 9 ):
        groups.append( list(x + i*9))
    for i in range(9):
        groups.append( list(x*9 + i) )
    groups.append(( 0, 1, 2, 9,10,18,19,20,29))
    groups.append(( 3, 4, 5,11,12,13,14,15,22))
    groups.append(( 6, 7, 8,16,17,24,25,26,33))
    groups.append((21,23,30,31,32,39,40,41,49))
    groups.append((27,28,36,37,38,47,48,56,57))
    groups.append((34,35,42,43,44,50,51,59,60))
    groups.append((45,46,54,55,63,64,72,73,74))
    groups.append((58,65,66,67,68,69,75,76,77))
    groups.append((52,53,61,62,70,71,78,79,80))
    return groups

def ConvertMat( mat ):
    # convert a matrix to a dictionary of boxes
    dct = {}
    # box = [answer,[choices]]
    k = 0
    V,H = mat.shape
    for i in range(V):
        for j in range(H):
            if mat[i,j] == -1:
                box = [-1,[1,2,3,4,5,6,7,8,9]]
            else:
                box = [mat[i,j],[]]
            dct[k] = box
            k += 1
    return dct

#%%
# Presenting information of the puzzle
def UnsolvedCount(dct):
    answ = 0
    for k in dct.keys():
        if dct[k][0] == -1:
            answ +=1
    return answ

def PrintSolution(dct,L=9):
    k = 0
    for i in range(L):
        for j in range(L):
            #print(dct[k][0],end=' ')
            print("{0:>3}".format(dct[k][0]),end='')
            k = k+ 1
        print('')


#%%
# Rule 1    
def AnswersInGroup( dct, groupsi ):
    # Collect the answers in groups[i]
    knowns = []
    for cellid in groupsi:
        if dct[cellid][0] != -1:
            knowns.append( dct[cellid][0] )
    return knowns

def RemovalInGroup( aig, dct, groupsi ):
    # remove choices in group if answers are set
    # aig from AnswersInGroup
    for cellid in groupsi:
        # consider each answer
        for j in aig:
            if j in dct[cellid][1]:
                # j is a set answer and it exists in block dct[i]
                dct[cellid][1].remove(j)
                    
def FindSolos(dct):
    ct = 0
    for cellid in dct.keys():
        if dct[cellid][0]==-1 and len(dct[cellid][1])==1:
            ct += 1
            dct[cellid][0] = dct[cellid][1].pop(0)
            print('rule 1', cellid,dct[cellid][0] )
    return ct  # if 0 then there were no changes

def Rule1( dct, groups ):
    for g in groups:
        aig = AnswersInGroup( dct, g )
        RemovalInGroup( aig, dct, g )
    ct = FindSolos( dct )
    return ct

def Rule2( dct, groups ):
    # for each group
    soli = [] # will contain those boxes that have single solutions
    for grp in groups:
        # get candidates
        cands = []
        for cellid in grp:
            if dct[cellid][0] == -1:
                cands.extend( dct[cellid][1] )
        # get unique candidates
        unq = list( set( cands ))
        # for each unique candidate
        #print(g,unq)
        for solveval in unq:
            # if the count is exactly 1
            if cands.count( solveval ) == 1:
                # then there is only one location for this solution
                for cellid in grp:
                    if solveval in dct[cellid][1]:
                        soli.append( (cellid,solveval) )
    soli = list(set(soli))
    print('Rule 2',soli)
    for i,q  in soli:
        dct[i][0] = q
        dct[i][1] = []
    # rule 2 not removing candidates
    # RemovalInGroup( aig, dct, groupsi )
#    RemoveFromRule2( hits, dct, groups )
                                   
#%%
def Rule3( dct, groups ):
    print('Rule 3')
    for grp in groups:
        tdct = {} # temp dictionary
        for gcell in grp:
            v = tuple(dct[gcell][1])  # candidates for this cell
            if v in tdct:
                tdct[v] += 1
            else:
                tdct[v] = 1
        for t in tdct:
            if len(t)==2 and tdct[t] == 2:
                # only remove if cell has something else
                    for gcell in grp:
                        if tuple(dct[gcell][1]) != t:
                            for tt in t:
                                if tt in dct[gcell][1]:
                                    dct[gcell][1].remove(tt)


#%%
def Sudoku(dct,groups):
    ok = True
    while ok:
        end1 = UnsolvedCount(dct)
        Rule1( dct, groups )
        end2 = UnsolvedCount(dct)
        if end2 == 0:
            ok = False
        if end1==end2:
            Rule2(dct,groups)
            end3 = UnsolvedCount(dct)
            if end1==end3:
                Rule3(dct,groups)
                end4 = UnsolvedCount(dct)
                if end1==end4:
                    ok = False                
    PrintSolution(dct)
#%%
def SudokuR1R2(dct,groups):
    ok = True
    while ok:
        end1 = UnsolvedCount(dct)
        Rule1( dct, groups )
        end2 = UnsolvedCount(dct)
        if end2 == 0:
            ok = False
        if end1==end2:
            hits=Rule2(dct,groups)
            end3 = UnsolvedCount(dct)
            #print('b',end2)
            if end1==end3:
                ok = False
    PrintSolution(dct)
#%%

	
def SwapCells(puzzle,val1,val2):
    ans = puzzle + 0
    v,h = (puzzle==val1).nonzero()
    ans[v,h] = val2
    v,h = (puzzle==val2).nonzero()
    ans[v,h] = val1
    return ans
	
def SwapBlockRows(puzzle, rndx1, rndx2 ):
    if rndx1 not in (0,3,6) or rndx2 not in (0,3,6):
        print('Index input must be 0,3,or 6')
        return 0
    ans = puzzle + 0
    for i in range(3):
        ans[[rndx1+i,rndx2+i]] = ans[[rndx2+i,rndx1+i]]
    return ans

# a[[2,0]] = a[[0,2]] # rows ::: a[:,[2,0]] = a[:,[0,2]] # columns
# puzzle2 = np.rot90(puzzle,1) 
# p2 = np.fliplr(puzzle); p3 = np.flipud(puzzle)

def TrivialSolution():
    puzzle = np.zeros((9,9),int)
    puzzle[0] = (1,2,3,4,5,6,7,8,9)
    puzzle[1] = (4,5,6,7,8,9,1,2,3)
    puzzle[2] = (7,8,9,1,2,3,4,5,6)
    puzzle[3] = (2,3,4,5,6,7,8,9,1)
    puzzle[4] = (5,6,7,8,9,1,2,3,4)
    puzzle[5] = (8,9,1,2,3,4,5,6,7)
    puzzle[6] = (3,4,5,6,7,8,9,1,2)
    puzzle[7] = (6,7,8,9,1,2,3,4,5)
    puzzle[8] = (9,1,2,3,4,5,6,7,8)
    return puzzle

def RemoveRandomCell(puzzle):
    v,h = (puzzle!=-1).nonzero()
    ndx = list(range(len(v)))
    r = np.random.choice(ndx)
    puzzle[v[r],h[r]] = -1
	
def CreatePuzzle(puz):
    groups = Architecture1()
    ok = True;     oldpuz = puz + 0
    while ok:
        RemoveRandomCell(puz)
        dct = ConvertMat(puz)
        Sudoku(dct,groups)
        a = UnsolvedCount(dct)
        if a!=0:
            ok=False;    #print(oldpuz)
        else:
            oldpuz = puz + 0
    return oldpuz


def Puzzle1():
    mat = np.array( (
        (-1,-1,7,9,6,2,4,-1,-1),
        (9,-1,-1,-1,1,-1,-1,-1,2),
        (-1,1,-1,8,5,3,-1,6,-1),
        (5,-1,-1,4,7,9,-1,-1,1),
        (-1,-1,-1,-1,8,-1,-1,-1,-1),
        (4,-1,-1,3,2,1,-1,-1,7),
        (-1,9,-1,2,4,8,-1,5,-1),
        (6,-1,-1,-1,3,-1,-1,-1,8),
        (-1,-1,8,6,9,5,1,-1,-1) ) )
    dct = ConvertMat(mat)
    return dct    

            
#mat, groups = Puzzle1()
#dct = ConvertMat(mat)
#Sudoku(dct,groups)
#print(EndGame(dct))