#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 21:46:42 2017

@author: timotheeaupetit
"""

import matplotlib.pyplot as plt

class RushHour:
    def __init__(self, x, y1, y2 = None):
        self.abscisse = x
        self.series1 = y1
        self.series2 = y2
        
    def graphe1(self):
        if self.series2:
            plt.plot(self.abscisse, self.series1, 'k', self.abscisse, self.series2, 'bo')
        else:
            plt.plot(self.abscisse, self.series1, 'k')
        plt.show()