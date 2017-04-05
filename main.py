#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:29:33 2016

@author: timotheeaupetit
"""

from supermarket import Supermarket

def main():
    supermarket = Supermarket() # we only need to create one supermarket
    Tnow = 0                    # time arbitrarily starts at 0
    supermarket.manageSupermarket(Tnow)
    
if __name__ == '__main__':
    main()
    