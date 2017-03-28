# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:29:33 2016

@author: timotheeaupetit
"""

class CMagasin():
    taille_caisse = 3 #taille d'une file d'attente à une caisse
    temps_magasin = 5
    temps_caisse = 4
        
    def __init__(self):
        self.caisses_utilisees = []
        self.nb_clients = 0
        
    def client_entre(self, d):
        self.nb_clients += 1
        print (self.nb_clients, 'client(s) en magasin')
        evt1 = CEvenement(d + self.calcul_delta(d), 1) #évènement prochain client
        evt2 = CEvenement(d + self.temps_magasin, 2) #évènement passage en caisse du client qui vient de rentrer

    def client_attend(self, d):
        self.nb_clients -= 1
        if len(self.caisses_utilisees) == 0:
            self.ouvrir_caisse()
            print(len(self.caisses_utilisees), 'caisse(s) ouverte(s)')
        caisse = self.choisir_caisse()
        taille_file = self.caisses_utilisees[caisse]
        if taille_file == self.taille_caisse:
            self.ouvrir_caisse()
            caisse = self.choisir_caisse()
        self.caisses_utilisees[caisse] += 1
        print (self.get_nb_in_caisses(), 'client(s) en caisse')
        
        taille_file = self.caisses_utilisees[caisse]
        evt = CEvenement(d + 5 * taille_file, 3, caisse)
    
    def client_paye(self, d, c):   
        evt = CEvenement(d + self.temps_caisse, 4, c) #évènement sortir de la caisse
        
    def client_sort(self, c):
        self.caisses_utilisees[c] -= 1
        if self.caisses_utilisees[c] == 0:
            self.fermer_caisse(c)
        
    def gerer_magasin(self, Tnow):
        event = CEvenement(Tnow, 1)
        while Tnow < 20: #len(event.liste_evt) > 0 #Tant qu'il y a des evenements à traiter
            print("Liste d'evenements :", event.liste_evt)
            print ('Date =', Tnow)
            for evt in event.liste_evt:
                type_evt = evt[1]
                caisse = evt[2]
                if evt[0] == Tnow:
                    if type_evt == 1: #arrivee client en magasin
                        self.client_entre(Tnow)
                        
                    if type_evt == 2: #arrivee client en file de caisse
                        self.client_attend(Tnow)          
        
                    if type_evt == 3: #passage en caisse
                        self.client_paye(Tnow, caisse)
        
                    if type_evt == 4: #sortie definitive
                        self.client_sort(caisse)
                        
                    event.sup_evt(Tnow, type_evt, caisse) #supprimer evenement courant
            
            Tnow += 1
            input ('Entree pour continuer')

    def calcul_delta(self, Tnow):
        if 0 <= Tnow and Tnow < 60: #Tnow compris entre 9h et 10h
            return 4
        if 60 <= Tnow and Tnow < 120: #Tnow compris entre 10h et 11h
            return 3
        if 120 <= Tnow and Tnow < 300: #Tnow compris entre 11h et 14h
            return 2
        if 360 <= Tnow and Tnow < 420: #Tnow est compris entre 14h et 15h
            return 4
        if 420 <= Tnow and Tnow < 480: #Tnow est compris entre 15h et 16h
            return 3
        if 480 <= Tnow and Tnow < 540: #Tnow est compris entre 16h et 17h
            return 3
        if 540 <= Tnow and Tnow < 600: #Tnow est compris entre 17h et 18h
            return 1
        if 600 <= Tnow and Tnow < 645: #Tnow est compris entre 18h et 18h44
            return 2

    def get_nb_in_caisses(self):
        nb = 0
        for caisse in self.caisses_utilisees:
            nb += self.get_nb_in_caisse(caisse)
        return nb
        
    def get_nb_in_caisse(self, caisse):
        return int(caisse)
        
    def choisir_caisse(self):
        self.index = 0
        self.plus_courte = self.taille_caisse
        
        for caisse in self.caisses_utilisees:
            if caisse < self.plus_courte:
                self.plus_courte = caisse
                return self.index               
            self.index +=1
            
    def ouvrir_caisse(self):
        self.caisses_utilisees.append(0)
        
    def fermer_caisse(self, c):
        self.caisses_utilissees.remove(c)

#-----------------------------------------------------------------
        
class CEvenement():
    liste_evt = []
    
    def __init__(self, d, t, c = None):
        self.liste_evt.append([d, t, c])
        self.liste_evt.sort()
       
#Supprime un evenement de la liste d'evenements
    def sup_evt(self, d, t, c):
        self.liste_evt.remove([d, t, c])

    def get_cur_evt(self, d):
        self.cur_evt = []
        for evt in self.liste_evt:
            if evt[0] == d:
                self.cur_evt.append(evt)
        return self.cur_evt
