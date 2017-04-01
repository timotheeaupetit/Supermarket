# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:29:33 2016

@author: timotheeaupetit
"""

class Supermarket():
    time_in_store = 5       # time a customer spends in the store
    time_at_checkout = 4    # time a customer spends to pay at the checkout
        
    def __init__(self):
        self.Events = []            # list of ordered events
        self.busyCheckouts = []     # list containing open checkouts
        self.customerCount = 0      # amount of customers in the store
        
    def manageSupermarket(self, Tnow):
        self.Events(Event(Tnow, 1))
        
        while Tnow < 20: #len(self.Events) > 0: # While remaining events
            print("Events:", self.Events)
            print ('Date =', Tnow)
            
            for evt in self.Events:
                type_evt = evt[1]
                checkout = evt[2]
                
                if evt[0] == Tnow:
                    if type_evt == 1: # customer go in
                        self.customer_Enter(Tnow)
                        
                    if type_evt == 2: # customer queue before checkout
                        self.customer_Queue(Tnow)          
        
                    if type_evt == 3: # customer pay
                        self.customer_Checkout(Tnow, checkout)
        
                    if type_evt == 4: # customer go out
                        self.customer_Exit(checkout)
                        
                    self.Events.remove([Tnow, type_evt, checkout]) #supprimer evenement courant
            
            Tnow += 1  
            
    def customer_Enter(self, d):
        """
        This method adds 1 to the customer count, then creates 2 events: 
            - the next customer's arrival
            - the current customer's move to checkout's buffer
        """
        self.customerCount += 1
        print (self.customerCount, 'customer(s) are shopping')
        
        self.Events.append(Event(d + self.timeToNextCustomer(d), 1)) # 'next customer' event
        self.Events.append(Event(d + Supermarket.time_in_store, 2)) # 'to queue' event, for current customer
        self.Events.sort()

    def customer_Queue(self, d):
        """
        This method remove 1 to the customer count...
        """
        self.customerCount -= 1
        
        if len(self.busyCheckouts) == 0:
            self.openCheckout()
            print(len(self.busyCheckouts), 'open checkout(s)')
            
        chk = self.chooseCheckout()
        
        if chk.queueSize == Checkout.queueCapacity:
            chk = self.openCheckout()
            
        chk.addToQueue()
        print (chk.queueSize, 'customer(s) are queuing')
        
        self.Events.append(Event(d + Checkout.checkoutDuration * chk.queueSize, 3, chk)) # 'checkout' event, for current customer
    
    def customer_Checkout(self, d, checkout):   
        checkout.removeFromQueue()
        self.Events.append(Event(d + Supermarket.time_at_checkout, 4, checkout)) # 'exit' event, for current customer
        
    def customer_Exit(self, checkout):
        
        if checkout.queueSize == 0:
            self.closeCheckout(checkout)
        
    def timeToNextCustomer(self, Tnow):
        """
        Calculate the time between each customer arrival, based on the hour range
        """
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
        """
        Returns the total amount of customers queuing before all checkouts
        """
        return sum(i.queueSize for i in self.busyCheckouts)
        
    def chooseCheckout(self):
        index = 0
        shortest = min(i.queueSize for i in self.busyCheckouts)
        
        for checkout in self.busyCheckouts:
            if checkout.queueSize == shortest:
                return self.busyCheckouts[index]          
            index += 1
    
    def openCheckout(self):
        chk = Checkout()
        self.busyCheckouts.append(chk)
        return chk
        
    def closeCheckout(self, checkout):
        self.busyCheckouts.remove(checkout)
        
#Supprime un evenement de la liste d'evenements
    def sup_evt(self, d, t, c):
        self.Events.remove([d, t, c])

    def get_cur_evt(self, d):
        self.cur_evt = []
        for evt in Event.liste_evt:
            if evt[0] == d:
                self.cur_evt.append(evt)
        return self.cur_evt
    
#-----------------------------------------------------------------
class Checkout():        
    queueCapacity = 3       # max size of a queue at a checkout
    checkoutDuration = 4    # time a customer spends to pay at the checkout
    
    def __init__(self):
        self.queueSize = 0      # size of a queue at a checkout
    
    def addToQueue(self):
        self.queueSize += 1
    
    def removeFromQueue(self):
        self.queueSize -= 1
#-----------------------------------------------------------------    
class Event(list):
    
    def __init__(self, d, t, c = None):
        """ Arguments are used as follows:
        - d: date of the event
        - t: type of event (1: Enter, 2: Queue, 3: Checkout or 4: Exit)
        - c: checkout number
        """
        self.append(d, t, c)