# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:35:54 2016

@author: mbremer
"""

import matplotlib.pyplot as plt
import numpy as np


def plotlinfit(x,y):
    par = np.polyfit(x, y, 1, full=True)

    slope=par[0][0]
    intercept=par[0][1]
    yfit = x*slope+intercept

    # calculate R squared and adjusted R2, which is better
    R2 = 1-np.sum((y-yfit)**2)/np.sum((y-np.mean(y))**2)
    adjR2 = R2-(1-R2)/(x.size-2)


    # make plots
    plt.scatter(x, y, s=30, alpha=0.9, marker='o')

    plt.plot(x,yfit, color = 'r')
    plt.text(min(x)-.1*(max(x)-min(x)) , max(y)-.1*(max(y)-min(y)),'adj. R^2 = %0.2f'% adjR2, fontsize=20)
    plt.text(min(x)-.1*(max(x)-min(x)) , max(y)-.2*(max(y)-min(y)),'slope {0:.2f}, intercept {1:.3f}'.format(slope,intercept), fontsize=14)

    plt.xlabel("X Description")
    plt.ylabel("Y Description")

    return slope, intercept


def plotR2(x,y):
    # determine best fit line
    par = np.polyfit(x, y, 1, full=True)

    slope=par[0][0]
    intercept=par[0][1]
    yfit = x*slope+intercept


    # calculate R squared and adjusted R2, which is better
    R2 = 1-np.sum((y-yfit)**2)/np.sum((y-np.mean(y))**2)
    adjR2 = R2-(1-R2)/(x.size-2)


    # make plots
    plt.scatter(x, y, s=30, alpha=0.9, marker='o')

    plt.plot(x,yfit, color = 'r')
    plt.text(min(x)-.1*(max(x)-min(x)) , max(y)-.1*(max(y)-min(y)),'$adj. R^2 = %0.2f$'% adjR2, fontsize=30)

    plt.xlabel("X Description")
    plt.ylabel("Y Description")

    return adjR2


def plotR2error(x,y,yerr):
    # determine best fit line
    par = np.polyfit(x, y, 1, full=True)

    slope=par[0][0]
    intercept=par[0][1]
    yfit = x*slope+intercept


    # calculate R squared and adjusted R2, which is better
    R2 = 1-np.sum((y-yfit)**2)/np.sum((y-np.mean(y))**2)
    adjR2 = R2-(1-R2)/(x.size-2)


    # make plots
    plt.errorbar(x, y, yerr, alpha=0.5, marker ='o',linestyle = 'none')

    plt.plot(x,yfit, color = 'r')
    plt.text(min(x)-.1*(max(x)-min(x)) , max(y)-.1*(max(y)-min(y))+max(yerr),'$adj. R^2 = %0.2f$'% adjR2, fontsize=30)

    plt.xlabel("X Description")
    plt.ylabel("Y Description")
    plt.xlim([min(x)-.1*(max(x)-min(x)), max(x)+.1*(max(x)-min(x))])
    plt.ylim([min(y)-.1*(max(y)-min(y))-max(yerr), max(y)+.1*(max(y)-min(y))+max(yerr)])



    return adjR2, slope, intercept