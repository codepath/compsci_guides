## Introduction

Stacks and queues are foundational data structures that are useful when adding and removing in particular orders. It's important to be comfortable with these two data structures.

## Stacks
A **stack** is a data structure that stores objects in which the most recently stored objects are the first ones to be removed, (LIFO: last in, first out). An example to help you remember the mechanics of a stack is to associate it with stacks in real life. With a stack of plates, the plates that are placed on top of a stack will be the first ones that are removed from the top!

![](https://i.imgur.com/qMSmxsa.png)

It's important to know the common operations of a stack. The two key stack operations are:
1) pop(): removing an item from the stack in a last in, first out order (LIFO)
2) push(item): adding an item to the stack


## Queues
A **queue** is a data structure that stores objects in which the most stored objects are the first ones to be removed. A helpful acronym associated with queues is FIFO, first in first out. An example to help you remember the mechanics of a queue is to associate it with queues in real life. With a queue of people waiting to get a seat in a restaurant, the first people to get in the queue will be the first people seated at that restaurant.

![](https://i.imgur.com/NKuZd0s.png)

It's important to know the common operations associated with a queue. The two important queue operations are:
1) dequeue(): removing an item from the queue in a first in, first out order (FIFO)
2) enqueue(item): adding an item to the queue

## Key takeaways
* Stacks are very useful for it's backtracking features. For example, parsing questions tend to use stacks because of the LIFO property.
* Stacks can be used to implement recursive solutions iteratively.
* Queues are useful when the ordering of the data matters as it preserves that ordering. For example, they're used for caching.

## Example problems
* Stacks: 
  * [Implement a queue with stacks](https://leetcode.com/problems/implement-queue-using-stacks/description/)

* Queues:
  * [LRU Cache](https://leetcode.com/problems/lru-cache/)

## Resources
### Guides
* [Overview of stacks & queues with applications](https://www.cs.cmu.edu/~adamchik/15-121/lectures/Stacks%20and%20Queues/Stacks%20and%20Queues.html)
* [In depth stacks guide](https://medium.com/basecs/stacks-and-overflows-dbcf7854dc67)
* [In depth queues guide](https://medium.com/basecs/to-queue-or-not-to-queue-2653bcde5b04)

### Libraries
* [Java queue library](https://docs.oracle.com/javase/7/docs/api/java/util/Queue.html)
* [Java stack library](
https://docs.oracle.com/javase/7/docs/api/java/util/Stack.html)
* [Python queue library](
https://docs.python.org/2/tutorial/datastructures.html#using-lists-as-queues)
* [Python stack library](https://docs.python.org/2/tutorial/datastructures.html#using-lists-as-stacks)

