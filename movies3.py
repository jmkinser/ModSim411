# movies.py
# JM Kinser
# version 3
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.


import pandas

def ReadData(fname):
    df = pandas.read_excel(fname,sheet_name='movies')
    movies = df.values
    df = pandas.read_excel(fname,sheet_name='actors')
    actors = df.values
    df = pandas.read_excel(fname,sheet_name='isin')
    isin = df.values.astype(int)
    return movies, actors, isin

# ########### Analysis Functions #################

# average:   avg = sum(inlist)/len(inlist)

def CombineLists( list1, list2 ):
    s1 = set(list1)
    s3 = s1.intersection( list2 )
    outlist = list( s3 )
    return outlist


# ########### Single input single output #################

def TitleFromMid( movies, mid ):
    tt = ''
    ndx = (movies[:,0]==mid).nonzero()[0]
    if len(ndx)>0:
        tt = movies[ndx[0]][1]
    return tt

def MidFromTitle( movies, title ):
    mid = 0
    ndx = (movies[:,1]==title).nonzero()[0]
    if len(ndx)>0:
        mid = movies[ndx[0]][0]
    return mid
    
def AidFromName( actors, firstname, lastname):
    aid = -1
    ndx1 = (actors[:,1]==firstname).nonzero()[0]
    ndx2 = (actors[:,2]==lastname).nonzero()[0]
    ndx = CombineLists( ndx1, ndx2 )
    if len(ndx)>0:
        aid = actors[ndx[0]][0]
    return aid

def NameFromAid( actors, aid ):
    ndx = (actors[:,0]==aid).nonzero()[0][0]
    return actors[ndx,1],actors[ndx,2]


# ############## Single Input - Multiple Output  #################
def AidsFromMid( isin, mid ):
    ndx = (isin[:,1]==mid).nonzero()[0]
    aids = isin[ndx,2]
    return aids

def MidsFromAid( isin, aid ):
    ndx = (isin[:,2]==aid).nonzero()[0]
    mids = isin[ndx,1]
    return mids

# ############## Multiple Inputs - Multiple Output  #################
def NamesFromAids( actors, aids ):
    names = []
    for a in aids:
        names.append( NameFromAid(actors,a))
    return names

def TitlesFromMids( movies, mids ):
    titles = []
    for m in mids:
        titles.append( TitleFromMid(movies,m))
    return titles

def AidsFromMids( isin, mids ):
    aids = []
    for m in mids:
        aids.extend( AidsFromMid( isin, m ))
    aids = list(set(aids))
    return aids

def MidsFromAids( isin, aids ):
    mids = []
    for a in aids:
        mids.extend( MidsFromAid(isin,a))
    mids = list(set(mids))
    return mids

# ############## Combinations  #################
def MoviesOfTwoActors(actors,isin,f1,l1, f2, l2):
    aid1 = AidFromName(actors,f1,l1)
    mids1 = MidsFromAid(isin,aid1)
    aid2 = AidFromName(actors,f2,l2)
    mids2 = MidsFromAid(isin,aid2)
    mids = CombineLists(mids1,mids2)
    return mids