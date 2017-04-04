# Supermarket
This is a supermarket customer flow simulator, initially developed in C++, in the frame of my Industrial Engineering studies. The flow statistical analysis is not (yet) implemented.

There is no asynchronous programming, but a list of events created all along the execution. Each event will have a date of occurence, a type and possibly a "checkout" reference.

Customers arrive at a certain rate given the hour range. 
Every customer:
- spends arbitrarily 5 time units in the supermarket
- spends arbitrarily 4 time units to pay (at checkout), hence if there are people queuing in front of him, his waiting time is deduced from the number of people in front of him
- chooses the checkout with the shortest queue

A checkout:
- has an id
- has a queue with a maximum size of 3 people
- opens when all other checkouts are full
- closes when empty
