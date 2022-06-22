# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:12:50 2020

@author: jkinser
"""
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.

#%%
# Download the HTML from Control U.
# remove tne <!-- and --> before and after the events.
# save the file 
#%%
import os
import copy
from lxml import html, etree
import requests
import math
import numpy as np
import urllib

# Getting Information from web pages
def DownLoadPage(url):
    response = urllib.request.urlopen(url)
    dat = str(response.read())
    return dat[4:-1]

def FindNextUrl( dat, team = 'Kansas City Athletics'):
    loc1 = dat.find('Next Game')
    loc2 = dat.find('Next Game',loc1+1)
    # one of these is correct
    loc3 = dat.find(team,loc1-400,loc1)
    if loc3==-1:
        loc1=loc2
        loc3 = dat.find(team,loc2-400)
    # move forward
    loc4 = dat.find('href',loc1-80)
    loc5a = dat.find('"',loc4)
    loc5b = dat.find('"',loc5a+1)
    #print(loc1,loc3,loc4,loc5a,loc5b)
    newurl = 'https://www.baseball-reference.com/'+dat[loc5a+2:loc5b]
    return newurl

def DownloadFiles(starturl, outdir, team='Washington Nationals', N=5):
    url = starturl
    for i in range(N):
        print(url)
        dat = DownLoadPage(url)
        n = url.rfind('/')
        nexturl = FindNextUrl(dat,team)
        fp = open(outdir + url[n:],'w')
        a = dat.split('\\'+'n') # newline is screwy in file
        a = '\n'.join(a)
        fp.write(a)
        url = nexturl
    return nexturl

# To get data directly from the webpage
# CUrrently NOT working
def SnarfWeb(urlname):
    webpage = requests.get(urlname)
    page = str(html.fromstring(webpage))
    print(len(page))
    page = page.replace('<!--\n','')
    page = page.replace('-->\n','')
    tree = html.fromstring(page)
    outs = tree.xpath('//td[@data-stat="outs"]/text()')
    onbase = tree.xpath('//td[@data-stat="runners_on_bases_pbp"]/text()')
    return outs, onbase

# #######################################3
# Collecting data from stored pages
def GetOutsBases(fname):
    with open(fname) as f:
        page = f.read()
    page = page.replace('<!--','')
    page = page.replace('-->','')
    tree = html.fromstring(page)
    outs = tree.xpath('//td[@data-stat="outs"]/text()')
    onbase = tree.xpath('//td[@data-stat="runners_on_bases_pbp"]/text()')
    # remove the top 5 plays
    outs = outs[5:]
    onbase = onbase[5:]
    return outs, onbase

def ToInnings(outs,onbase):
    innings = []
    N = len(outs)
    st = [outs[0] + onbase[0]]
    for i in range(1,N):
        if outs[i]=='0' and outs[i-1]!='0':
            st.append('3---')
            innings.append( st )
            st = ['0---']
        else:
            tostring = outs[i] + onbase[i]
            st.append(tostring)
    # last atbats
    st.append('3---')
    innings.append(st)
    return innings

def AddEvent(fromstring,tostring,dct):
    if fromstring not in dct:
        d = {}
        d[tostring] = 1
        dct[fromstring] = d
    else:
        if tostring not in dct[fromstring]:
            dct[fromstring][tostring] = 1
        else:
            dct[fromstring][tostring] += 1

def EventCounts(innings,dct):
    NI = len(innings) # number of innings
    for i in range(NI):
        fromstring = innings[i][0]
        for j in range(1,len(innings[i])):
            tostring = innings[i][j]
            AddEvent(fromstring,tostring,dct)
            fromstring = tostring

# ############################################
# BUilding the HMM
#%%
def GetCounts(mydir):
    games = GetGames(mydir)
    dct = {}
    for i in range(len(games)):
        outs, onbase = GetOutsBases(games[i])
        innings = ToInnings(outs,onbase)
        #print(games[i],len(outs))
        print('.',end='')
        EventCounts(innings,dct)
    return dct
#dct = GetCounts(mydir)
#%%
# convert the dictionary to probabilities
def ToProbs(dct):
    probs = copy.deepcopy( dct )
    for k in probs.keys():
        # sum of all entries
        sm = 0
        for k2 in probs[k].keys():
            sm += probs[k][k2]
        # probbilities
        for k2 in probs[k].keys():
            probs[k][k2] = probs[k][k2] / sm
    return probs

def EventProbs(trail,probs):
    p = 1
    for t in range(len(trail)-1):
        p *= probs[trail[t]][trail[t+1]]
    return p
# nat 7th inning WS game 7
#trail = ('0---','1---','1---','11--','1---','11--','112-','212-','3---')
# print( EventProbs(trail,probs))

# ########################################
# functions for a season            
def GetGames(mydir):
    a = os.listdir(mydir)
    games = []
    for i in a:
        if '.shtml' in i:
            games.append(mydir+'/'+i)
    return games

# Find the strangest inning:  Lowest logodds
def StrangeInning(datadir, probs):
    least = 999999
    strange = []
    games = GetGames(datadir)    
    for i in range(len(games)):
        outs, onbase = GetOutsBases(games[i])
        innings = ToInnings(outs,onbase)
        print('.',end='')
        for j in range(len(innings)):
            pb = 1
            for k in range(len(innings[j])-1):
                fromstring = innings[j][k]
                tostring = innings[j][k+1]
                pb *= probs[fromstring][tostring]
            if pb == least:
                strange.append(innings[j])
            if pb < least:
                least = pb
                strange = [innings[j]]
    return least, strange
