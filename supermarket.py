#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:29:33 2016

@author: timotheeaupetit
"""
from graphs import RushHour

class Supermarket(object):
    
    time_in_store = 5       # arbitrary time a customer spends in the store
    time_at_checkout = 4    # arbitrary time a customer spends at the checkout (not in the queue before the checkout)
        
    def __init__(self):
        self.Events = []            # list of events
        self.busyCheckouts = []     # list containing open checkouts
        self.customerInStore = 0    # amount of customers in the store
        self.customerShopping = 0   # amount of customers shopping    
        self.time = []
        self.customerCount = []
        self.checkoutCount = []
        
    def manageSupermarket(self, Tnow):
        self.Events.append(Event(Tnow, 1)) # initial Event
        
        while len(self.Events) > 0: # While remaining events
            self.Events.sort(key=lambda x: x[0]) # reorder events by their dates
            
#            print ('\nDate =', Tnow)    
#            print("Events:", self.Events)
#            print(self.customerShopping, 'customer(s) are shopping')
#            print(self.getQueueSizes(), 'customer(s) are queuing')
#            print(len(self.busyCheckouts), 'open checkout(s)')
            
            oldEvents = []
            
            for evt in self.Events:
                if evt[0] == Tnow:
                    
                    type_evt = evt[1]
                    checkout = evt[2]
                    
                    oldEvents.append(evt) # memorize current event to delete it outside of the loop
                    
                    if type_evt == 1:               # customer go in
                        self.customer_Enter(Tnow)
                        
                    if type_evt == 2:               # customer queue before checkout
                        self.customer_Queue(Tnow)          
        
                    if type_evt == 3:               # customer pay
                        self.customer_Checkout(Tnow, checkout)
        
                    if type_evt == 4:               # customer go out
                        self.customer_Exit(checkout)
            
            self.Events = [evt for evt in self.Events if evt not in oldEvents]
            
            self.time.append(Tnow)
            self.customerCount.append(self.customerInStore)
            self.checkoutCount.append(len(self.busyCheckouts))
            
            Tnow += 1  
            #input('Press enter to continue')
            
        statistics = RushHour(self.time, self.customerCount, self.checkoutCount)
        statistics.graphe1()
            
    def customer_Enter(self, d):
        """
        This method adds 1 to the customer count, then creates 2 events: 
            - the next customer's arrival
            - the current customer's move to checkout's buffer
        """
        self.customerInStore += 1
        self.customerShopping += 1
        
        if d < 645:
            self.Events.append(Event(d + Supermarket.timeToNextCustomer(d), 1)) # 'next customer' event
            self.Events.append(Event(d + Supermarket.time_in_store, 2)) # 'to queue' event, for current customer

    def customer_Queue(self, d):
        """
        Defines what happens when a customer has finished shopping and reaches the queues
        """
        self.customerShopping -= 1
        
        if len(self.busyCheckouts) == 0:
            chk = self.openCheckout()
        else:
            chk = self.chooseCheckout()
            if chk.queueSize == Checkout.queueCapacity:
                chk = self.openCheckout()
            
        chk.addToQueue()
        
        if d < 645:
            self.Events.append(Event(d + Checkout.checkoutDuration * chk.queueSize, 3, chk)) # 'checkout' event, for current customer
    
    def customer_Checkout(self, d, chk):
        """
        Defines what happens when a customer exits the queue and reaches the checkout
        """
        chk.removeFromQueue() # remove one customer from the chk queue
        if d < 645:
            self.Events.append(Event(d + Supermarket.time_at_checkout, 4, chk)) # 'exit' event, for current customer
        
    def customer_Exit(self, chk):
        """
        Defines what happens when a customer exits the checkout (and therefore the supermarket)
        """
        #print('1 customer exit from checkout', chk.id, '\n')
        self.customerInStore -= 1
        if chk.queueSize == 0:
            self.closeCheckout(chk)
                
    def openCheckout(self):
        """
        Creates a new checkout, appends it to the list of open checkouts an return it
        """
        chk = Checkout()
        self.busyCheckouts.append(chk)
        return chk

    def chooseCheckout(self):
        """
        Returns the checkout which has the shortest queue
        """
        index = 0
        shortest = min(chk.queueSize for chk in self.busyCheckouts)
        
        for chk in self.busyCheckouts:
            if chk.queueSize == shortest:
                return self.busyCheckouts[index]          
            
            index += 1
  
    def closeCheckout(self, chk):
        """
        Closes the checkout passed in argument (removal from busyCheckouts list)
        """
        self.busyCheckouts.remove(chk)        
      
    def getQueueSizes(self):
        """
        Returns the total amount of customers queuing before all checkouts
        """
        return sum(chk.queueSize for chk in self.busyCheckouts)

    def timeToNextCustomer(Tnow):
        """
        Calculates the time between each customer arrival, based on the hour range
        """
        if Tnow < 60:     #Tnow between 9-10am
            return 4
        elif Tnow < 120:  #Tnow between 10-11am
            return 3
        elif Tnow < 300:  #Tnow between 11am-2pm
            return 2
        elif Tnow < 420:  #Tnow between 2-3pm
            return 4
        elif Tnow < 480:  #Tnow between 3-4pm
            return 3
        elif Tnow < 540:  #Tnow between 4-5pm
            return 3
        elif Tnow < 600:  #Tnow between 5-6pm
            return 1
        elif Tnow < 645:  #Tnow between 6-6:44pm
            return 2
        else: 
            return None

#-----------------------------------------------------------------
class Checkout(object):        
    
    queueCapacity = 3       # max size of a queue at a checkout
    checkoutDuration = 4    # time a customer spends to pay at the checkout
    checkoutID = 0
    
    def __init__(self):
        self.queueSize = 0      # size of a queue at a checkout
        self.id = Checkout.checkoutID
        Checkout.checkoutID += 1
    
    def addToQueue(self):
        self.queueSize += 1
    
    def removeFromQueue(self):
        self.queueSize -= 1
        
    def __repr__(self):
        return str(self.id) #+ ' ('+ str(self.queueSize)+')'
    
#-----------------------------------------------------------------    
class Event(tuple):
    """ 
    An Event is a tuple (read only) of 3 elements:
        - d: date of the event
        - t: type of event (1: Enter, 2: Queue, 3: Checkout or 4: Exit)
        - c: checkout object (None by default)
    """
    def __new__ (cls, d, t, c = None):
        return super(Event, cls).__new__(cls, tuple([d, t, c]))

    # the __init__ method is called from the tuple class, so there is no need to redefine it here
