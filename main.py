# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:29:33 2016

@author: timotheeaupetit
"""

from classes import CMagasin

def main():
    mag = CMagasin()
    Tnow = 0
    mag.gerer_magasin(Tnow)
    
if __name__ == '__main__':
    main()