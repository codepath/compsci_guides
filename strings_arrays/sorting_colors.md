## Problem
Given N objects colored red, white and blue, sort them *in-place* in red-white-blue order.

Red, white, and blue objects are represented as 0, 1, and 2 respectively.

Example:
```python
>>> colors = [2, 1, 2, 0, 0, 1]
>>> sort_colors(colors)
>>> colors
[0, 0, 1, 1, 2, 2]
```

## Approach #1: Merge or quick sort

**Approach**
The problem is asking us to sort a list of integers, so we could potentially use an algorithm like merge sort or quick sort. 

**Time and space complexity**
With a sorting algorithm such as is O(N log N) in the worst case. The space complexity is O(1) since we sort in place.

## Approach #2: Counting sort
**Approach**
We know that the numbers we are sorting are 0, 1, or 2. This leads to an efficient counting sort implementation, since we can just count the numbers of each and modify the list in place to match the counts in sorted order.

**Implementation**
```python
from collections import defaultdict
def sort_colors(colors):
    counts = defaultdict(int)
    for num in colors:
        counts[num] += 1
    idx = 0
    while idx < counts[0]:
        colors[idx] = 0
        idx += 1
    while idx < counts[0] + counts[1]:
        colors[idx] = 1
        idx += 1
    while idx < counts[0] + counts[1] + counts[2]:
        colors[idx] = 2
        idx += 1
```

**Time and space complexity**
This solution has complexity O(N), since we loop through the list once, then loop through the dictionary to modify our list, both of which take N time. This solution takes up O(1) space, since everything is done in place and the counts dictionary has a constant size.

## Approach #3: Three-way partition
This approach uses multiple pointers. Reading the [two pointer guide](https://guides.codepath.com/compsci/Two-pointer) may be helpful.

**Approach**
Although we cannot asymptotically do better than O(N) since we need to pass through the list at least once, we can limit our code to only making one pass. This will be slightly faster than approach #2.

We can accomplish this by seeing that sorting an array with three distinct elements is equivalent to a `partition` operation. Recall that in quick sort, we partition an array to put all elements less than a pivot to the left and greater than to a right. Since we only have three potential values in our list, partitioning using the middle value as a pivot will effectively sort the list.

This particular type of partition is a bit tricky though because we're partitioning on the middle element (the 1's) of our list. It's called a three-way partition, since we are also grouping together elements that are equal in the middle (the 1's).


**Implementation**

```python
def sort_colors(colors):
    left, middle, right = 0, 0, len(colors) - 1
    while middle <= right:
        if colors[middle] == 0:
            colors[middle], colors[left] = colors[left], colors[middle] 
            left += 1
            middle += 1
        elif colors[middle] == 1:
            middle += 1
        elif colors[middle] == 2:
            colors[middle], colors[right] = colors[right], colors[middle] 
            right -= 1
            middle += 1
```


**Time and space complexity**
This solution has also has complexity O(N), but only takes one pass since it uses two pointers that stop moving when one moves past the other.

It is slightly faster than the counting sort and is O(1) space, since it is in-place.

**Note:** This problem is also known as the [Dutch flag problem](https://en.wikipedia.org/wiki/Dutch_national_flag_problem).
