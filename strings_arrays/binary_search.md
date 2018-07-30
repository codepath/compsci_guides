Binary search is a technique for efficiently locating an element in a sorted list. Searching for an element can done naively in **O(n)** time by checking every element in the list, but binary search's optimization speeds it up to **O(log n)**. Binary search is a great tool to keep in mind for array problems.

Algorithm
------------------
In binary search, you are provided a sorted list of numbers and a key. The desired output of a binary search is the index of the key in the sorted list, if the key is in the list, or ```None``` otherwise.

Binary search is a recursive algorithm. From a high-level perspective, we examine the middle element of the list, which determines whether to terminate the algorithm (found the key), recursively search the left half of the list (middle element value > key), or recursively search the right half of the list (middle element value < key).
```
def binary_search(nums, key):
    if nums is empty:
        return None
    if middle element is equal to key:
        return middle index
    if middle element is greater than key:
        binary search left half of nums
    if middle element is less than
        binary search right half of nums
```

There are two canonical ways of implementing binary search: recursive and iterative. Both solutions utilizes two pointers that keep track of the portion of the list we are searching.

### Recursive Binary Search

The recursive approach utilizes a helper function to keep track of pointers to the section of the list we are currently examining. The search either terminates when we find the key or if the two pointers meet.

```python
def binary_search(nums, key):
    return binary_search_helper(nums, key, 0, len(nums))

def binary_search_helper(nums, key, start_idx, end_idx):
    middle_idx = (start_idx + end_idx) // 2
    if start_idx == end_idx:
        return None
    if nums[middle_idx] > key:
        return binary_search_helper(nums, key, start_idx, middle_idx)
    elif nums[middle_idx] < key:
        return binary_search_helper(nums, key, middle_idx + 1, end_idx)
    else:
        return middle_idx
```

### Iterative Binary Search

The iterative approach manually keeps track of the section of the list we are examining using the two-pointer technique. The search either terminates when we find the key, or the two pointers meet.
```python
def binary_search(nums, key):
    left_idx, right_idx = 0, len(nums)
    while right_idx > left_idx:
        middle_idx = (left_idx + right_idx) // 2
        if nums[middle_idx] > key:
            right_idx = middle_idx
        elif nums[middle_idx] < key:
            left_idx = middle_idx + 1
        else:
            return middle_idx
    return None
```

## Runtime and Space Complexity

Binary search has **O(log n)** time complexity because each iteration decreases the size of the list by a factor of 2. Its space complexity is constant because we only need to maintain two pointers. Even the recursive solution has constant space with [tail call optimization](https://en.wikipedia.org/wiki/Tail_call).

## Example problems
* [Search insert position](https://leetcode.com/problems/search-insert-position/description/)
* [Search in a 2D matrix](https://leetcode.com/problems/search-a-2d-matrix/description/)

## Video walkthrough
* [HackerRank binary search video](https://www.youtube.com/watch?v=P3YID7liBug)
* [Question walkthrough: Search a 2D matrix](https://www.youtube.com/playlist?list=PL7zKQzeqjecINi-_8CmiFLMLCCxjIHBPj)
* [Question walkthrough: Ice Cream Parlor](https://youtu.be/Ifwf3DBN1sc)
