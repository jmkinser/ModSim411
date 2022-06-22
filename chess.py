# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:22:43 2020

@author: jkinser
"""
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


# ##########  CHESS

import copy
import numpy as np
#%%
def PieceValues():
    values = {}
    values['p'] = 1
    values['r'] = 8
    values['n'] = 5
    values['b'] = 5
    values['q'] = 10
    values['k'] = 500
    return values   
#%%
def BlankChess(values):
    blank = [' .',0]
    board = np.zeros((8,8),type(blank))
    for i in range(8):
        for j in range(8):
            board[i,j] = blank
    return board
#%%
def InitChess(values):
    blank = [' .',0]
    board = np.zeros((8,8),type(blank))
    for i in range(8):
        for j in range(8):
            board[i,j] = blank
    board[0,0] = ['br1',values['r']] # creates a rook.  black rook #1
    board[0,1] = ['bn1',values['n']] # knight
    board[0,2] = ['bb1',values['b']] # bishop
    board[0,3] = ['bq',values['q']] # queen
    board[0,4] = ['bk',values['k']] # king
    board[0,5] = ['bb2',values['b']]
    board[0,6] = ['bn2',values['n']]
    board[0,7] = ['br2',values['r']]
    for i in range(8):
        board[1,i] = ['bp'+str(i+1),1]
    board[7,0] = ['wr1',values['r']] # creates a rook.  black rook #1
    board[7,1] = ['wn1',values['n']] # knight
    board[7,2] = ['wb1',values['b']] # bishop
    board[7,3] = ['wq',values['q']] # queen
    board[7,4] = ['wk',values['k']] # king
    board[7,5] = ['wb2',values['b']]
    board[7,6] = ['wn2',values['n']]
    board[7,7] = ['wr2',values['r']]
    for i in range(8):
        board[6,i] = ['wp'+str(i+1),1]
    return board
#%%
def PrintBoard(board):
    for v in range(8):
        for h in range(8):
            print('%5s' % board[v,h][0], end='')
        print('')
#%%
# assume the move is legal
def Move(board, oldloc, newloc):
    # old location and new location
    nam,val = ' .',0
    if board[oldloc][0] != ' .':
        nam, val = board[newloc] # get the name of the piece
        board[newloc] = board[oldloc] # move piece
        board[oldloc] = [' .',0]
    return nam,val # piece that was removed
#%%
def PawnMove(board, i,j ):
    poss = [] # possible moves
    bw = board[i][j][0][0] # black or white
    if bw == 'b':
        # piece is coming down the board
        # move one space if unoccupied
        if board[i+1][j][0] == ' .':
            poss.append((i+1,j))
        # move two spaces if unoccupied and at row 1
        if i==1 and board[i+2][j][0]== ' .' and board[i+1][j][0]==' .':
            poss.append((i+2,j))
        # capture one space
        if j-1>=0:
            if board[i+1][j-1][0][0]=='w':
                poss.append((i+1,j-1))
        if j+1<8:
            if board[i+1][j+1][0][0]=='w':
                poss.append((i+1,j+1))
    # repeat for white
    if bw=='w':
        if board[i-1][j][0]==' .':
            poss.append((i-1,j))
        if i==6 and board[i-2][j][0]==' .' and board[i-1][j][0]==' .':
            poss.append((i-2,j))
        if j+1<8:
            if board[i-1][j+1][0][0]=='b':
                poss.append((i-1,j+1))
        if j-1>=0:
            if board[i-1][j-1][0][0]=='b':
                poss.append((i-1,j-1))
    return poss
#%%
def GoFar(board,i,j,poss,kk,ll):
    bw = board[i][j][0][0]
    # move up left
    ok = True
    k = i;l=j
    while ok:
        k += kk; l+= ll
        if k<0 or l<0 or k>7 or l>7:
            ok = False
            break # you have reached the end of the board        
        if board[k][l][0]==' .':
            poss.append((k,l))  # open space
        if (board[k][l][0][0]=='w' and bw=='b') or (board[k][l][0][0]=='b' and bw=='w'):
            poss.append((k,l)) # atrack
            ok = False
            break
        if board[k][l][0][0]== bw:
            ok = False
            break
    # don't need to return poss
    
def RookMove(board,i,j):
    poss = []
    GoFar(board,i,j,poss,-1, 0)
    GoFar(board,i,j,poss, 1, 0)
    GoFar(board,i,j,poss, 0,-1)
    GoFar(board,i,j,poss, 0, 1)
    return poss

    
def BishopMove(board, i,j):
    poss = []
    GoFar(board,i,j,poss,-1,-1)
    GoFar(board,i,j,poss,-1, 1)
    GoFar(board,i,j,poss, 1,-1)
    GoFar(board,i,j,poss, 1, 1)
    return poss

def QueenMove(board,i,j):
    poss = RookMove(board,i,j)
    poss.extend( BishopMove(board,i,j))
    return poss
#%%
def KnightMove(board,i,j):
    bw = board[i][j][0][0]
    poss = []
    allowed = ((1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(-2,-1),(2,-1))
    for kk,ll in allowed:
        k = i+kk; l=j+ll
        if k<0 or k>7 or l<0 or l>7:
            pass # off the board
        elif board[k][l][0][0]==bw:
            # landing on your on piece
            pass
        else:
            poss.append((k,l)) 
    return poss
#%%
def KingMove(board,i,j):
    bw = board[i][j][0][0]
    poss = []
    for kk in range(-1,2):
        for ll in range(-1,2):
            k = i+kk; l=j+ll
            if k<0 or k>7 or l<0 or l>7:
                pass # off the board
            elif board[k][l][0][0]==bw:
                # landing on your on piece
                pass
            else:
                poss.append((k,l)) 
    return poss
#%%
def ScoreActivePieces(board):
    white = 0; black = 0
    # go through each tile
    for i in range(8):
        for j in range(8):
            bw = board[i][j][0][0] # b or w
            if bw=='w':
                white += board[i][j][1]
            if bw=='b':
                black += board[i][j][1]
    return black,white
#%%
def AllPossible(board, i,j):
    # decode piece and determine which function to use
    p = board[i][j][0][1]
    if p=='p':
        poss = PawnMove(board,i,j)
    if p=='r':
        poss = RookMove(board,i,j)
    if p=='n':
        poss = KnightMove(board,i,j)
    if p=='b':
        poss = BishopMove(board,i,j)
    if p=='q':
        poss = QueenMove(board,i,j)
    if p=='k':
        poss = KingMove(board,i,j)
    return poss
#%%
# score center control.
# score pieces in 2x2 middle
# consider all pieces and all their possible moves.  Score these.
def ScoreCenterControl(board):
    black, white = 0,0
    for i in range(3,5):
        for j in range(3,5):
            bw = board[i][j][0][0] # b or w
            if bw=='w':
                white += board[i][j][1]
            if bw=='b':
                black += board[i][j][1]
    # find the pieces that can get to the center of the board.
    for i in range(8):
        for j in range(8):
            poss=[]  # init because a piece may not be able to move
            # if there is a piece, find all possible moves
            if board[i][j][0] != ' .':
                poss = AllPossible(board,i,j)
            # pare down to just the center four and score
            for ii,jj in poss:
                if 3<=ii<=4 and 3<=jj<=4:
                    bw = board[i][j][0][0]
                    if bw=='w':
                        white += board[i][j][1]
                    if bw=='b':
                        black += board[i][j][1]
    return black, white
#%%
# score how many points are in immediate peril
def ScorePeril(board):
    black, white = 0,0
    # go through all pieces
    for i in range(8):
        for j in range(8):
            # is there a piece at this position?
            if board[i][j][0]!=' .':
                # get possible moves for this piece
                poss = AllPossible(board,i,j)
                # for each move determine if it captures an opponent
                bw = board[i][j][0][0] # color of current piece
                for px,py in poss:
                    pbw = board[px][py][0][0] # color on target square
                    if pbw != bw and pbw != ' ':
                        # score capture
                        if bw=='b':
                            black += board[px][py][1]
                        if bw=='w':
                            white += board[px][py][1]
    return black, white
#%%
def Score(board, player='b'):
    # default is black player.  for white use player=0
    # return score as a percentage B/(B+W)
    b1,w1 = ScoreActivePieces(board)
    b2,w2 = ScoreCenterControl(board)
    b3,w3 = ScorePeril(board)
    #print('Scores', b1,w1, b2,w2, b3,w3)
    # more points possible for Active than other two methods.  Scale by 5
    b = b1+5*b2+5*b3; w =w1+5*w2+5*w3
    r = np.random.rand()*0.01 # to break ties
    if player=='b':
        pct = b/(b+w+r)
    else:
        pct = w/(b+w+r)
    return pct
#%%
# score the possible moves
def ScoreMoves(board, player='b'):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j][0][0] == player:
                # this is a black piece
                poss = AllPossible(board,i,j) # all moves for this piece
                for ii,jj in poss:
                    tempboard = copy.deepcopy(board) # reset board
                    Move(tempboard,(i,j),(ii,jj))
                    score = Score(tempboard,player) # score this 
                    moves.append((board[i][j][0],(i,j),(ii,jj),score))
    return moves
#%%
def PickMove(moves):
    best = []; bestsc = 0
    for m in moves:
        if m[3]>bestsc:
            bestsc = m[3]
            best = copy.deepcopy(m)
    # second best move 0 just for grins
    best2, best2sc = [],0
    for m in moves:
        if m[3]>best2sc and m[3]<bestsc:
            best2sc = m[3]
            best2 = copy.deepcopy(m)
    return best, best2
#%%
def SortMoves(moves):
    NMoves = len(moves)
    scores = np.zeros( NMoves )
    for i in range( NMoves ):
        scores[i] = moves[i][3] # collect scores
    ndx = scores.argsort()
    ndx = ndx[::-1]
    answ = []
    for i in ndx:
        answ.append( moves[i] )
    return answ

#%%
def PickMoveFrom5(moves):
    smoves = SortMoves( moves )
    p = [0,1,2,3,4]
    me = np.random.choice(p)
    return smoves[me]
