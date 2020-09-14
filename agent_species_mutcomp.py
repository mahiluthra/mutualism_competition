# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 14:36:19 2019

@author: mahi

"""

import numpy as np

class CLV():

    def __init__(self, n):
        self.n = n                                              # Number of species
        self.x = np.random.normal(0.5,0.1,self.n)               # Species population
        self.alphax = np.random.normal(1,0.1,(self.n,self.n))    # Interactions
        self.k = np.random.normal(1,0.1,self.n)                 # Carrying capacity
        self.rx = np.random.normal(1,0.1,self.n)                 # Growth rate
        
        self.h = 1
        self.gamma =  np.random.normal(1,0.1,(self.n, self.n))
        
        self.y = np.random.normal(0.5,0.1,self.n)               # Species population
        self.alphay = np.random.normal(1,0.1,(self.n,self.n))    # Interactions
        self.ry = np.random.normal(1,0.1,self.n)

    def step_competition(self, dt):
        # competition differential equation
        dxdt = self.r*self.x*(1 - (np.dot(self.alpha, self.x))/self.k)
        self.x += dt * dxdt
        
    def step_mutualism(self, dt):
        # mutualism differential equation
        growth = self.rx * self.x
        competition = self.rx * self.x * np.dot(self.alphax,self.x)
        mutualism = ( self.rx * self.x * np.dot(self.gamma, self.y)) / (1 + self.h * np.dot(self.gamma , self.y))
        dxdt = growth - competition + mutualism
        self.x += dt * dxdt
        
        growth = self.ry * self.y
        competition =  self.ry * self.y * np.dot(self.alphay,self.y)
        mutualism = ( self.ry * self.y * np.dot(np.transpose(self.gamma), self.x)) / (1 + self.h * np.dot(np.transpose(self.gamma) , self.x))
        dydt = growth - competition + mutualism
        self.y += dt * dydt        

    def resetState(self):
        self.x = np.random.normal(0.5,0.1,self.n)
        self.y = np.random.normal(0.5,0.1,self.n)
    
    def diversity(self):
        return len(np.where(self.x > 0.01)[0])
    
    def delInteractions(self,p):
        for i in range(self.n):
            for j in range(self.n):
                if (i!=j and np.random.rand()<p):
                    self.alpha[i][j] = 0

    # For evolution
    def setParams(self,params):
        k = 0
        for i in range(self.n):
            for j in range(self.n):
                if i!=j:
                    self.alphax[i][j] = (params[k]/4) + 1.0
                    k += 1
                else:
                    self.alphax[i][j] = 1.0
                    
        for i in range(self.n):
            for j in range(self.n):
                if i!=j:
                    self.alphay[i][j] = (params[k]/4) + 1.0
                    k += 1
                else:
                    self.alphay[i][j] = 1.0
                    
        for i in range(self.n):
           for j in range(self.n):
                   self.gamma[i][j] = (params[k]/4) + 1.0
                   k += 1

        for i in range(self.n):
            self.rx[i] = (params[k]/4) + 1.0
            k += 1
            
        for i in range(self.n):
            self.ry[i] = (params[k]/4) + 1.0
            k += 1
        
        for i in range(self.n):
            self.k[i] = 1.0