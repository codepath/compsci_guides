## Arrays
An **array** is a data structure that holds a fixed number of objects. Because arrays have fixed sizes, they are highly efficient for quick lookups regardless of how big the array is. However, there is a tradeoff with this fast access time; any insertion or deletion from the middle of the array requires moving the rest of the elements to fill in or close the gap. To optimize time efficiency, try to add and delete mostly from the end of the array.

Arrays commonly come up in interviews, so it's important to review the array library for the language you code in.

**Tips:**
* Off-by-one errors can often happen with arrays, so be wary of potentially over indexing as it will throw an error
* Try to add elements to the back of an array instead of the front, as adding to the front requires shifting every element back
* In Java, arrays are a fixed size so consider utilizing an [ArrayList](https://docs.oracle.com/javase/8/docs/api/java/util/ArrayList.html) instead if you need to dynamically alter the size of the array. 

## Strings
**Strings** are a special kind of array, one that only contains characters. They commonly come up in interview questions, so it's important to go through the string library for the language you're most comfortable with. You should know common operations such as: getting the length, getting a substring, splitting a string based on a delimiter, etc.

It's important to note that whenever you mutate a string, a new copy of the string is created. There are different ways to reduce the space utilized depending on the language:
* In Python, you can represent a string as a list of characters and operate on the list of character instead.
* In Java, you can utilize the [StringBuffer](https://docs.oracle.com/javase/7/docs/api/java/lang/StringBuffer.html) class to mitigate the amount of space utilized if you need to mutate a string.

## Patterns List
* [Two pointer](https://guides.codepath.com/compsci/Two-pointer)
* [Binary Search](https://guides.codepath.com/compsci/Binary-Search)

### Strings
#### General guide
* [Coding for Interviews Strings Guide](http://blog.codingforinterviews.com/string-questions/)

#### Strings in C++
   * [Character Arrays in C++](https://www.youtube.com/watch?v=Bf8a6IC1dE8)
   * [Character Arrays in C++ Part 2](https://www.youtube.com/watch?v=vFZTxvUoZSU)

### Arrays
#### General guide
 * [InterviewCake Arrays](https://www.interviewcake.com/concept/java/array)

#### Python arrays
* [Google developer lists guide](https://developers.google.com/edu/python/lists)
#### Java arrays
 * [InterviewCake DynamicArray](https://www.interviewcake.com/concept/java/dynamic-array-amortized-analysis?)
 * [ArrayList Succinctly Guide](https://code.tutsplus.com/tutorials/the-array-list--cms-20661)
