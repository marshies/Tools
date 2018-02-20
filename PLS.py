# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 10:14:37 2016

@author: mbremer
"""

import numpy as np

def PLS(spectra, known_values, numcomps):
    
    WW=np.empty([spectra.shape[1],numcomps])
    PP=np.empty([spectra.shape[1],numcomps])
    qq=np.empty([1,numcomps])
    
    #initial weight guess
    ww = np.dot(np.transpose(spectra),known_values)
    ww = ww/np.linalg.norm(ww)

    # initial scores
    tt = np.dot(spectra,ww)
        
    
    for i in range(0,numcomps):
        # normalize scores
        ti = np.dot(np.transpose(tt),tt)
        tt = tt/ti
    
        # principle component vector
        pp = np.dot(np.transpose(spectra),tt)
        PP[:,i] = pp[:,0] # all PC vectors
    
        # principle vector of Y? Y-weights
        qi = np.dot(np.transpose(known_values),tt)
        qq[:,i]=qi
    
        WW[:,i] = ww[:,0] #all the weights
    
        # deflate X
        spectra = spectra-ti*tt*np.transpose(pp)
        ww = np.dot(np.transpose(spectra),known_values) # new weights
        tt = np.dot(spectra,ww) # new scores
        continue
        
    P=np.dot(np.transpose(PP),WW)#So that the opperations were successful    
    WWp = np.dot(WW,np.linalg.inv(P))
    BB = np.dot(WWp,np.transpose(qq))
    

    return BB
