# Heaps

## Introduction
Heaps are an often overlooked data structure, but come up quite often in interview problems. **Heaps** are special tree based data structures that satisfy two properties:

1. All nodes are ordered in a specific way, depending on the type of heap. There are two types of heaps: min heaps and max heaps.
    *  In **min heaps**, the root node contains the smallest element and all the nodes in the heap contain elements that are less than their child nodes.
    * In **max heaps**, the root node contains the largest element and all the nodes in the heap contain elements that are greater than their child nodes.

2. It is a complete binary tree. A **binary treeâs** nodes will have at most two children: a left child, and right child. A heap is a complete binary tree, which means that it fills each level entirely except the last level. Another way of thinking about this is that all the nodes in one level will have children before any of those nodes will have grandchildren.

[Insert diagram here of min heap/ max heap]

## Heap Operations
In order to understand the runtimes of heap operations, it is vital to understand how insertion and deletion work within a heap.

### Insertion
When a new element is inserted into a heap, it is added in the next empty spot in the heap, in the left most position in the last level of the heap, in order to maintain the full shape of the heap. However, this new item may violate the other key property of the heap, its ordering.

In a min heap, if the parent of the new element is greater than it, it gets swapped with the parent. This element keeps getting **bubbled up** in the tree until it either reaches the root of the heap or it has been placed in the right order. This same process applies to max heaps as well, but the check to ensure that the node is in the proper position is that the parent node is greater than the new node.

[Diagram of a swapping procedure]

### Removal
When removing from a heap, the root node is always removed. Then, the last element, the leftmost node in the last level of the heap, is removed and set as the root. This removal process retains the heap shape, but this new ordering may violate the proper ordering of the heap.

In a min heap, if either one of the new element's children are less than their parent, the new element is swapped with the smaller of the two children. This element keeps getting **bubbled down** in the tree until it either reaches the last level of the heap or it has been placed in the right position. The same process applies to max heaps as well, but the ordering is such that the children are both greater than the current node.

[Diagram of a swapping procedure]

### Building a heap from a list
One approach to building a heap from a list of N elements is starting with an empty heap and adding each item from a list, one at a time. This approach takes O(N log N) time because it performs N insertions, each of which takes log N time. However, this approach is suboptimal and the optimal approach of building a heap from N items only takes O(N) time!

The math and implementation behind this optimization are a bit complex, but are explained well in the [Wikipedia page](https://en.wikipedia.org/wiki/Binary_heap#Building_a_heap). Itâs a good idea to get a general understanding of the optimization.

## Implementation
Surprisingly, this complex data structure can be represented using an array! Given that the root node will always be either the least or greatest element in the heap, we can place this element as the first element in the array. This underlying array is then filled up by going through each level of the heap, from left to right, top to bottom.

With the guarantee of fullness and the binary tree property of the heap, we can easily calculate the indices of the children and parents of each node using these formulas:
* Parent: (current index - 2) / 2
* Left child: (current index * 2) + 1
* Right child: (current index * 2) + 2

[insert diagram here]

These calculations enable it to easily implement the insertion and removal procedures within the array.

## Runtimes
In the worst case scenario, the swapping procedure for insertions and deletions will move the element through the height of the heap. Because heaps are binary trees that are guaranteed to be as complete as possible, the number of levels in the heap will be log n.


| Operation                           | Runtime  |
| ------------------------------------| -------- |
| Reading largest or smallest element | O(1)     |
| Insertion                           | O(log n) |
| Deletion                            | O(log n) |
| Creating a heap from a list         | O(n)     |

## Key takeaways
* Heaps are especially useful when for getting the largest or smallest elements, and in situations where you donât care about fast lookup, delete, or search.
* Heaps are especially useful for questions that involve getting the x-largest or x-smallest elements of some data set.
* Building a heap only takes O(n) time, so you can potentially optimize a solution by building a heap from a list instead of running insertion n times to create the heap.

## Glossary
**Binary tree**: a tree that has at most two children.
**Bubble down**: the process of moving an element down within the heap by swapping it with one of its children until it is placed in the proper position that satisfies the heap ordering.
**Bubble up**: the process of moving an element up within the heap by swapping it with its parent until it is placed in the proper position that satisfies the heap ordering.
**Max heap**: tree based structure in which the root node contains the largest element and all the nodes in the heap contain elements that are greater than their child nodes.
**Min heap**: tree based structure in which the root node contains the smallest element and all the nodes in the heap contain elements that are less than their child nodes.

## Example problems
* [Top K frequent words](https://leetcode.com/problems/top-k-frequent-words/description/)
* [Find K pairs with smallest sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/)
* [Implementing a heap](http://interactivepython.org/courselib/static/pythonds/Trees/BinaryHeapImplementation.html)

## Resources
To get a more thorough understanding of the internals of heaps, here are a few links to helpful resources.
* Guide on heaps, with helpful diagrams: https://medium.com/basecs/learning-to-love-heaps-cef2b273a238
* Princeton Coursera video lecture series: https://www.coursera.org/learn/algorithms-part1/lecture/Uzwy6/binary-heaps
* HackerRank video: https://youtu.be/t0Cq6tVNRBA
