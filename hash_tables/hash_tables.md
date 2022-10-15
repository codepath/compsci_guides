## Introduction
**Hash tables** are one of the most common and useful data structures in both interviews and real life. The biggest advantage of hash tables is that they provide quick key-to-value lookup.

One use of a hash table would be to implement a phone book. In this scenario, the key is a name and the value is a phone number.

```python
address_book = {}
address_book["Bob"] = "111-222-3333"
address_book["Alice"] = "444-555-6666"
address_book.get("Bob")
'111-222-3333'
```

Hash tables are very efficient.  Operations such as insertion, deletion, and get take, on average, constant time.

## How it works:
### Hash Codes
Internally,a hash table stores its values in an array. A special **hash function** is utilized to convert each key into a code, which is then converted into an index into the underlying array. This hash function has a hard requirement to return the same hash code for equal keys.

Hash function generate a code, known as the **hash code**. Each data type will have its own hash function that generates its hash code differently. It is important to remember that a hash code is not equivalent to the index in the underlying array storage structure--there are often more hash codes than indices in the underlying array.

**Figure below**: Internals of a hash table
![](https://i.imgur.com/bEIWPaQ.png)


**Note:** When utilizing a hash table with a class you've created, be sure that the hash function for that object type operates as you would expect. If two objects are equivalent, you should ensure that their hash codes are the same.


### Collisions
If the hash function is implemented well, inputted objects will be distributed evenly across the array indices. However, the number of hash codes is often greater than the size of the underlying array, so some keys will be assigned the same index. When two keys are matched to the same index, this is called a **collision**. There are several different ways of addressing collisions. 

There are multiple approaches to dealing with collisions. The most common one is simply to store all the objects that get assigned to the same index in a linked list. In this scenario, instead of simply storing the value at that index, the linked list must contain both the entire key and the value in pairs instead of just the value, so that the values can be uniquely tied to a key.

**Figure below**: Hash Collision
![](https://i.imgur.com/ZqF2crs.png)

For more information about other ways to address hash collisions, see the [hash tables Wikipedia page](https://en.wikipedia.org/wiki/Hash_table#Open_addressing) for descriptions of several different approaches. If you have time, I'd encourage you to learn about open addressing, the other common hash collision method.

**Note on updating keys in the hash table**: Be wary of updating a key object that's present in the hash table. Once it's updated, lookup will no longer work for that key. Instead, if a key needs to be updated, remove it, update the key, then re-insert the key into the table.

## Runtimes
For interviews, it is generally assumed that the hash table is a well formed one, with few collisions. However, in the worst case scenario, all operations can take linear time. When a hash table distributes the objects poorly, all the objects may hash to the same index in the underlying array and any operation would require going through all of the previous entries.

|           | Lookup   | Insert   | Delete   |
| --------  | -------- | -------- | -------- |
| Best Case | O(1)     | O(1)     | O(1)     |
| Worst Case| O(n)     | O(n)     | O(n)     |


## Key takeaways
* Hash tables are an extremely useful data structure-- keep them in mind as a tool for most interview questions
* Hash tables have the best performance for lookups, inserts, and deletions. All three operations on average take O(1) time.

## Resources
To get a more thorough understanding on the internals of hash tables, here are a few links to helpful resources.
* Hash table guide with helpful diagrams: https://medium.com/basecs/hashing-out-hash-functions-ea5dd8beb4dd
* Princeton Coursera video lecture series: https://www.coursera.org/learn/algorithms-part1/lecture/CMLqa/hash-tables
* HackerRank video (short summary): https://youtu.be/shs0KM3wKv8
