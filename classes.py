# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:29:33 2016

@author: timotheeaupetit
"""

class Supermarket():
    checkout_size = 3       # max size of a queue at a checkout
    time_in_store = 5       # time a customer spends in the store
    time_at_checkout = 4    # time a customer spends to pay at the checkout
        
    def __init__(self):
        self.busy_Checkout = []
        self.customer_count = 0      # amount of customers in the store
        
    def customer_Enter(self, d):
        self.customer_count += 1
        print (self.customer_count, 'customer(s) are shopping')
        evt1 = Event(d + self.timeToNextCustomer(d), 1) # 'next customer' event
        evt2 = Event(d + Supermarket.time_in_store, 2) # 'to queue' event, for current customer

    def customer_Queue(self, d):
        self.customer_count -= 1
        if len(self.busy_Checkout) == 0:
            self.openCheckout()
            print(len(self.busy_Checkout), 'open checkout(s)')
        caisse = self.chooseCheckout()
        queueSize = self.busy_Checkout[caisse]
        if queueSize == Supermarket.checkout_size:
            self.openCheckout()
            caisse = self.chooseCheckout()
        self.busy_Checkout[caisse] += 1
        print (self.getQueueSize(caisse), 'customer(s) are queuing')
        
        queueSize = self.busy_Checkout[caisse]
        evt = Event(d + 5 * queueSize, 3, caisse) # 'checkout' event, for current customer
    
    def client_Checkout(self, d, c):   
        evt = Event(d + Supermarket.time_at_checkout, 4, c) # 'exit' event, for current customer
        
    def customer_Exit(self, c):
        self.busy_Checkout[c] -= 1
        if self.busy_Checkout[c] == 0:
            self.closeCheckout(c)
        
    def manageSupermarket(self, Tnow):
        event = Event(Tnow, 1)
        while Tnow < 20: #len(event.liste_evt) > 0: #Tant qu'il y a des evenements à traiter
            print("Events:", event.liste_evt)
            print ('Date =', Tnow)
            for evt in event.liste_evt:
                type_evt = evt[1]
                caisse = evt[2]
                if evt[0] == Tnow:
                    if type_evt == 1: #arrivee client en magasin
                        self.customer_Enter(Tnow)
                        
                    if type_evt == 2: #arrivee client en file de caisse
                        self.customer_Queue(Tnow)          
        
                    if type_evt == 3: #passage en caisse
                        self.client_Checkout(Tnow, caisse)
        
                    if type_evt == 4: #sortie definitive
                        self.customer_Exit(caisse)
                        
                    event.sup_evt(Tnow, type_evt, caisse) #supprimer evenement courant
            
            Tnow += 1

    def timeToNextCustomer(self, Tnow):
        if 0 <= Tnow and Tnow < 60:     #Tnow between 9-10am
            return 4
        if 60 <= Tnow and Tnow < 120:   #Tnow between 10-11am
            return 3
        if 120 <= Tnow and Tnow < 300:  #Tnow between 11am-2pm
            return 2
        if 360 <= Tnow and Tnow < 420:  #Tnow between 2-3pm
            return 4
        if 420 <= Tnow and Tnow < 480:  #Tnow between 3-4pm
            return 3
        if 480 <= Tnow and Tnow < 540:  #Tnow between 4-5pm
            return 3
        if 540 <= Tnow and Tnow < 600:  #Tnow between 5-6pm
            return 1
        if 600 <= Tnow and Tnow < 645:  #Tnow between 6-6:44pm
            return 2

    def getQueueSizes(self):
        return sum(int(i) for i in self.busy_Checkout)
        
    def getQueueSize(self, caisse):
        return int(caisse)
        
    def chooseCheckout(self):
        self.index = 0
        shortest = Supermarket.checkout_size
        
        for caisse in self.busy_Checkout:
            if caisse < shortest:
                shortest = caisse
                return self.index            
            self.index +=1
    
    def openCheckout(self):
        self.busy_Checkout.append(0)
        
    def closeCheckout(self, c):
        self.caisses_utilissees.remove(c)

#-----------------------------------------------------------------
        
class Event():
    liste_evt = []
    
    def __init__(self, d, t, c = None):
        """ Arguments are used as follows:
        - d: date of the event
        - t: type of event (1: Enter, 2: Queue, 3: Checkout or 4: Exit)
        - c: checkout number
        """
        Event.liste_evt.append([d, t, c])
        Event.liste_evt.sort()
       
#Supprime un evenement de la liste d'evenements
    def sup_evt(self, d, t, c):
        Event.liste_evt.remove([d, t, c])

    def get_cur_evt(self, d):
        self.cur_evt = []
        for evt in Event.liste_evt:
            if evt[0] == d:
                self.cur_evt.append(evt)
        return self.cur_evt
