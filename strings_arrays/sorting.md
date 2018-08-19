Sorting is a fundamental tool for tackling problems, and is often utilized to help simplify problems.

There are several different sorting algorithms, each with different tradeoffs. In this guide, we will cover several well-known sorting algorithms along with when they are useful.

We will describe merge sort and quick sort in detail and the remainder of the featured sorting algorithms at a high level.

## Terminology
Two commonly used terms in sorting are:

1. **in-place sort**: modifies the input list and does not return a new list
2. **stable sort**: retains the order of duplicate elements after the sort ([3, <u>2</u>, 4, **2**] -> [<u>2</u>, **2**, 3, 4])

## Merge sort
**Merge sort** is perhaps the simplest sort to implement and has very consistent behavior. It adopts a divide-and-conquer strategy: recursively sort each half of the list, and then perform an O(n) merging operation to create a fully sorted list.

### Implementation

The key operation in merge sort is `merge`, which is a function that takes two sorted lists and returns a single sorted list composed of elements of the combined lists.
```python
def merge(list1, list2):
    if len(list1) == 0:
        return list2
    if len(list2) == 0:
        return list1
    if list1[0] < list2[0]:
        return [list1[0]] + merge(list1[1:], list2)
    else:
        return [list2[0]] + merge(list1, list2[1:])
```
This is a recursive implementation of `merge`, but an iterative implementation will also work.

Given this `merge` operation, writing merge sort is quite simple.

```python
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    middle_idx = len(nums) // 2
    left_sorted = merge_sort(nums[:middle_idx])
    right_sorted = merge_sort(nums[middle_idx:])
    return merge(left_sorted, right_sorted)
```

### Runtime
Merge sort is a recursive, divide and conquer algorithm. It takes O(log n) recursive merge sorts and each merge is O(n) time, so we have a final runtime of O(n log n) for merge sort. Its behavior is consistent regardless of the input list (its worst case and best case take the same amount of time).

**Summary**

| Worst case | Best case | Stable | In-place|
|:----------:|:---------:|:------:|:-------:|
| O(n log n) | O(n log n) | ✅ | ❌ |

## Quick sort

**Quick sort** is also a divide and conquer strategy, but uses a two-pointer swapping technique instead of `merge`. The core idea of quick sort is selecting a "pivot" element in the list (typically the middle element), and swapping elements in the list such that everything left of the pivot is less than it, and everything right of the pivot is greater. We call this operation `partition`. Quick sort is notable for its ability to sort efficiently in-place.

```python
def partition(nums, left_idx, right_idx):
    pivot = nums[left_idx]
    while True:
        while nums[left_idx] < pivot and left_idx <= right_idx:
            left_idx += 1
        while nums[right_idx] > pivot and right_idx >= left_idx:
            right_idx -= 1
        if left_idx >= right_idx:
            return right_idx
        nums[left_idx], nums[right_idx] = nums[right_idx], nums[left_idx]
        left_idx += 1
        right_idx -= 1
```
The partition function modifies `nums` in-place and requires no extra memory. It also takes O(n) time worst case to fully partition a list.

```python
def quick_sort_helper(nums, left_idx, right_idx):
    if left_idx >= right_idx:
        return
    pivot_idx = partition(nums, left_idx, right_idx)
    if left_idx < pivot_idx - 1:
        quick_sort_helper(nums, left_idx, pivot_idx)
    if right_idx > pivot_idx + 1:
        quick_sort_helper(nums, pivot_idx + 1, right_idx)

def quick_sort(nums):
    quick_sort_helper(nums, 0, len(nums) - 1)
```

### Runtime

The best case performance of quick sort is O(n log n), but depending on the structure of the list, quick sort's performance can vary.

If the pivot happens to be the median of the list, then the list will be divided in half after the partition.

In the worst case, however, the list will be divided into an N - 1 length list and an empty list. Thus, in the worst possible case, quick sort has O(N<sup>2</sup>) performance, since we'll have to recursively quicksort (N - 1), (N - 2), ... many lists. However, on average and in practice, quick sort is still very fast due to how fast swapping array elements is.

The space complexity for this version of quick sort os O(log N), due to the number of call stacks created during recursion, but an iterative version can make space complexity O(1).

**Summary**

| Worst case | Best case | Stable | In-place|
|:----------:|:---------:|:------:|:-------:|
| O(n<sup>2</sup>) | O(n log n)| ❌ |  ✅ |

## Insertion sort

In **insertion sort**, we incrementally build a sorted list from the unsorted list. We take elements from the unsorted list and insert them into the sorted list, making sure to maintain the order.

This algorithm takes O(n<sup>2</sup>) worst time, because looping through the unsorted list takes O(n) and finding the proper place to insert can take O(n) time in the worst case. However, if the list is already sorted, insertion sort takes O(n) time, since insertion time will be O(1). Insertion sort can be done in-place, so it takes up O(1) space.

Insertion sort is easier on linked lists, which have O(1) insertion whereas arrays have O(n) insertion because in an array, inserting an element requires shifting all the elements behind that element.

**Summary**

| Worst case | Best case | Stable | In-place|
|:----------:|:---------:|:------:|:-------:|
| O(n<sup>2</sup>) | O(n)| ✅ |  ✅ |

## Selection sort

**Selection sort** incrementally builds a sorted list by finding the minimum value in the rest of the list, and swapping it to be in the front.

It takes O(n<sup>2</sup>) time in general, because we have to loop through the unsorted list which is O(n) and in each iteration, we search the rest of the list which always takes O(n). Selection sort can be done in-place, so it takes up O(1) space.

| Worst case | Best case | Stable | In-place|
|:----------:|:---------:|:------:|:-------:|
| O(n<sup>2</sup>) |  O(N<sup>2</sup>)| ❌ |  ✅ |

## Radix sort

**Radix sort** is a situational sorting algorithm when you know that the numbers you are sorting are bounded in some way. It operates by grouping numbers in the list by digit, looping through the digits in some order.

For example, if we had the list ```[100, 10, 1]```, radix sort would put 100 in the group which had 1 in the 100s digit place and would put (10, 1) in a group which had 0 in the 100s digit place. It would then sort by the 10s digit place, and finally the 1s digit place.

Radix sort thus needs one pass for each digit place it is sorting and takes O(KN) time, where K is the number of passes necessary to cover all digits.

| Worst case | Best case | Stable | In-place|
|:----------:|:---------:|:------:|:-------:|
| O(kn) |  O(kn)| ✅ (if going through digits from right to left) |  ❌ |

## Summary

|Sort | Worst case | Best case | Stable | In-place|
|:-:||:----------:|:---------:|:------:|:-------:|
|Merge sort | O(n log n) | O(n log n) | ✅ | ❌ |
|Quick sort | O(n<sup>2</sup>) | O(n log n)| ❌ |  ✅ |
| Insertion sort | O(n<sup>2</sup>) | O(n)| ✅ |  ✅ |
|Selection sort | O(n<sup>2</sup>) |  O(N<sup>2</sup>)| ❌ |  ✅ |
|Radix sort| O(kn) |  O(kn)| ✅ (if going through digits from right to left) |  ❌ |
