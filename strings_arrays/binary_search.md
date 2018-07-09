Binary search is a method for locating an element in a sorted list efficiently. Searching for an element can done naively in **O(N)** time, but binary search speeds it up to **O(log N)**. Binary search is a great tool to keep in mind for array problems.

Algorithm
------------------
In binary search, you are provided a list of sorted numbers and a key. The desired output is the index of the key, if it exists and None if it doesn't.

Binary search is a recursive algorithm. The high level approach is that we examine the middle element of the list. The value of the middle element determines whether to terminate the algorithm (found the key), recursively search the left half of the list, or recursively search the right half of the list.
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

The recursive solution utilizes a helper function to keep track of pointers to the section of the list we are currently examining. The search either completes when we find the key, or the two pointers meet.

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

The iterative solution manually keeps track of the section of the list we are examining, using the two-pointer technique. The search either completes when we find the key, or the two pointers meet.
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

Binary search completes in **O(log N)** time because each iteration decreases the size of the list by a factor of 2. Its space complexity is constant because  we only need to maintain two pointers to locations in the list. Even the recursive solution has constant space with [tail call optimization](https://en.wikipedia.org/wiki/Tail_call).

## Example problems
* [Search insert position](https://leetcode.com/problems/search-insert-position/description/)
* [Search in a 2D matrix](https://leetcode.com/problems/search-a-2d-matrix/description/)

## Video walkthrough
* [HackerRank binary search video](https://www.youtube.com/watch?v=P3YID7liBug)
* [Question walkthrough: Search a 2D matrix](https://www.youtube.com/playlist?list=PL7zKQzeqjecINi-_8CmiFLMLCCxjIHBPj)
* [Question walkthrough: Ice Cream Parlor](https://youtu.be/Ifwf3DBN1sc)
