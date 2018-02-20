# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 20:10:18 2016

@author: mbremer
"""
import numpy as np


def meancenter(spectra):
    return spectra - np.mean(spectra,0)

def SNV(spectra):
    return spectra/np.std(spectra,0)

def MSC(spectra,refspec=None):
    if refspec == None:
        refspec = np.mean(spectra,1)
    fit = np.polyfit(refspec,spectra,1)
    return (spectra-fit[1,:])/fit[0,:]

def remove_outliers(spectra, known_values, stdsaway = 2):
    initialnumber = spectra.shape[1]
    fff = spectra.reshape([spectra.shape[0],5,-1])
    spectrameans = np.mean(fff,1)
    spectrastds = np.std(fff,1)
    outlier_matrix = (np.rollaxis(fff,1,0)>spectrameans+stdsaway*spectrastds) + \
            (np.rollaxis(fff,1,0)<spectrameans-stdsaway*spectrastds)

    nonoutliers = (np.sum(outlier_matrix,1)<5).ravel()

    known_values = known_values[nonoutliers]
    spectra = spectra[:,nonoutliers]


    print('removed ' + str(initialnumber - np.sum(nonoutliers)) + ' outliers' )

    return spectra, known_values


