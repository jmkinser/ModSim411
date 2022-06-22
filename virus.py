# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 14:37:52 2021

@author: jkinser
"""
# (C) Jason Kinser 2022.
# This code is intended for non-commercial use in courses at George Mason Univ.
# Their are no guarantees with this code
# Commercial and/or non-academic use prohibited without written permission from the author.

import numpy as np

# # Create Class for a single person
class Person:
    def __init__(self):
        self.x = np.random.rand(2)*99
        self.v = np.random.rand(2)*10+5
        self.a = np.zeros(2)
        self.alive = True
        self.infected = False
        self.immune = False
        self.health = np.random.randint(50,150)
        self.bottom = np.random.randint(-50,100)
    def __str__( self ):
        st = ''
        temps = vars(self)
        for item in temps:
            st += str(item) + ': ' + str(temps[item]) + '\n'
        return st
    def Move(self, dt = 0.1):
        self.x = self.x + self.v*dt + 0.5*self.a*dt*dt
    def Boundaries(self,V,H):
        if self.x[0]<0: 
            self.x[0] *= -1
            self.v[0] *= -1
        if self.x[0] > H:
            self.x[0] = H - (self.x[0]-H)
            self.v[0] *= -1
        if self.x[1] < 0:
            self.x[1] *= -1
            self.v[1] *= -1
        if self.x[1] > V:
            self.x[1] = V - (self.x[1]-V)
            self.v[1] *= -1
    def LowerHealth(self):
        # lower health
        if self.infected==True and self.health>self.bottom:
            self.health -= 1
    def Cured(self):
        if self.health <= self.bottom:
            self.infected = False
            self.immune = True
    def Death(self):
        if self.health < 0:
            self.alive = False
    def Distance(self, you ):
        dist = np.sqrt(((self.x-you.x)**2).sum())
        return dist
    def Collide(self,you):
        ypart = you.x[1] - self.x[1]
        xpart = you.x[0] - self.x[0]
        alpha = np.arctan2( ypart, xpart )    
        R = np.array(((np.cos(-alpha),-np.sin(-alpha)),
                      (np.sin(-alpha),np.cos(-alpha))))
        vrot = R.dot( self.v)
        wrot = vrot * np.array((1,-1))
        R = np.array(((np.cos(alpha),-np.sin(alpha)),
                      (np.sin(alpha),np.cos(alpha))))
        w = R.dot(wrot)
        self.v = w +0
        # transfer infection
        if you.infected == True and self.immune==False:
            self.infected = True 

#%%
############################################
def CreateWorld( NPeople=100, V=100, H=100):
    people = []
    for i in range( NPeople ):
        people.append( Person() )
    return people

#%%
def Iterate( people, V, H ):
    for me in people:
        if me.alive:
            me.Move()
            me.Boundaries(V,H)
            me.LowerHealth()
            me.Cured()
            me.Death()
            # check for collision
            for you in people:
                if you.alive == True and me!=you:
                    if me.Distance(you) < 1:
                        me.Collide( you )
                        you.Collide( me )
        
#%%
# #############################################
# Matrix version
# ############################################

def InitVirusMats(NPeople = 100):
    M = np.zeros((NPeople,6)) # x, v, a
    B = np.zeros((NPeople,3), bool) # alive, infected, immune
    I = np.zeros((NPeople,2),int) # health bottom
    # set up random people
    M[:,:2] = np.random.ranf((NPeople,2))*99
    M[:,2:4] = np.random.ranf((NPeople,2))*10+5
    I[:,0] = np.random.randint(50,150,NPeople)
    I[:,1] = np.random.randint(-50,100,NPeople)
    B[:,0] = True # everyone is alive
    B[:,1] = False # not infected
    B[:,2] = False # not immune
    return M, B, I
	
def CollideM(M,B,me, him):
    #print(me,him)
    alpha = np.arctan2(M[him,1]-M[me,1],M[him,0]-M[me,0])
    R = np.array(((np.cos(-alpha),-np.sin(-alpha)),(np.sin(-alpha),np.cos(-alpha))))
    vrot = R.dot(M[me,2:4])
    wrot = vrot * np.array((1,-1))
    R = np.array(((np.cos(alpha),-np.sin(alpha)),(np.sin(alpha),np.cos(alpha))))
    w = R.dot(wrot)
    M[me,2:4] = w +0
    # transfer infection
    if B[him,1]==True and B[me,2]==False:
        B[me,1] = True

def IterateM(M,B,I):
    dt = 0.1
    X,Y = 100,100
    alive = B[:,0].nonzero()[0] # index of the living
    for me in alive:
        # move me
        M[me,:2] = M[me,:2] + M[me,2:4]*dt + 0.5*M[me,4:6]*dt**2
        # out of bounds
        if M[me,0]<0: 
            M[me,0] *= -1
            M[me,2] *= -1
        if M[me,0]>X: 
            M[me,0] = X - (M[me,0] -X)
            M[me,2] *= -1
        if M[me,1]<0: 
            M[me,1] *= -1
            M[me,3] *= -1
        if M[me,1]>Y: 
            M[me,1] = Y - (M[me,1] -Y)
            M[me,3] *= -1
        # lower health
        if B[me,1]==True and I[me,0]>I[me,1]:
            I[me,0] -= 1
        # cured
        if I[me,0]<=I[me,1]:
            B[me,1:3] = False, True
        # compute distant to all living
        them = list(alive)
        them.remove(me)
        them = np.array(them)
        
        dist = np.sqrt(((M[me,:2]-M[:,:2])**2).sum(1))
        closendx = (dist<1).nonzero()[0]
        for i in closendx:
            if i in them:
                CollideM(M,B,me,i)
                CollideM(M,B,i,me)
        # check for death
        ndx = (I[:,0]<=0).nonzero()[0]
        B[ndx] = False,False,False
#%%
def RunMatrixVirus(NPeople=300,NITERS=200):
    M,B,I = InitVirusMats(NPeople)
    B[:10,1] = True
    inf = np.zeros(NITERS)
    aliv = np.zeros(NITERS)
    for i in range( NITERS ):
        IterateM(M,B,I)
        inf[i] = B[:,1].sum()
        aliv[i] = B[:,0].sum()
    #plt.plot(inf)
    #plt.plot(aliv)
    #plt.show()
    return M,B,I, inf, aliv
    
#M,B,I, inf, aliv = RunMatrixVirus()

