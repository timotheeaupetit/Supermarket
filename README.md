# Supermarket
This is a supermarket customer flow simulator, initially developed in C++, in the frame of my Industrial Engineering studies. 

The entire program is based on the successive creation of events, which are stored in a list, that is scanned through a loop.
From a given event, a set of new events can be created (ex: when a customer comes in, the event "customer goes to queue" is created. It will happen 5 time units later).
The program stops when all the events have been scanned one by one.
That's minimalistic and deterministic, but I have a few ideas to make it more fun.

Anyway, each event is a list of 3 parameters which are:
- a date of occurence, 
- a type (1: a customer comes in, 2: a customer queues, 3: a customer pays at checkout, 4: a customer exits)
- and possibly a reference to an object "checkout".

Every customer:
- arrives at a certain interval given the hour range,
- spends arbitrarily 5 time units in the supermarket,
- spends arbitrarily 4 time units to checkout. If there are people queuing in front of him, his waiting time is calculated from the number of people in front of him,
- chooses the checkout with the shortest queue

A checkout:
- has an id,
- has a queue with a maximum size of 3 people,
- opens when all other checkouts are full,
- closes when empty

The subsequent statistical analysis is not (yet) implemented.