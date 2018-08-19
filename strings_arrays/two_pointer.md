The **two pointer method** is a helpful technique to keep in mind when working with strings and arrays. It's a clever optimization that can help reduce time complexity with no added space complexity (a win-win!) by utilizing extra pointers to avoid repetitive operations.

This approach is best demonstrated through a walkthrough, as done below.

## Problem: Minimum size subarray sum

Given an array of n positive integers and a positive integer s, find the minimal length of a contiguous subarray of which the sum ≥ s. If there isn't one, return 0 instead.

**Example:**
```python
>>> min_sub_array_length([2,3,1,2,4,3], 7)
2
```

Explanation: the subarray [4,3] has the minimal length under the problem constraint.

## Solution #1: Brute Force
### Approach

When first given a problem, if an optimal solution is not immediately clear, it's better to have any solution that works than be stuck. With this problem, a brute force solution would be to generate all possible subarrays and find the length of the shortest subarray that sums up to a sum that is greater than or equal to the given number.

### Implementation
```python
def min_sub_array_length(nums, sum):
    min_length = float("inf")
    for start_idx in range(len(nums)):
        for end_idx in range(start_idx, len(nums)):
            subarray_sum = get_sum(nums, start_idx, end_idx)
            if subarray_sum >= sum:
                min_length = min(min_length, end_idx - start_idx + 1)
    return min_length if min_length != float("inf") else 0

def get_sum(nums, start_index, end_index):
    result = 0
    for i in range(start_index, end_index + 1):
        result += nums[i]
    return result
```

### Time and space complexity

The time complexity of this solution would be O(n<sup>3</sup>). The double for loop results in O(n<sup>2</sup>) calls to get_sum and each call to get_sum has a worst case run time of O(n), which results in a O(n<sup>2</sup> * n) = **O(n<sup>3</sup>) runtime**.

The space complexity would be **O(1)** because the solution doesn't create new data structures.

## Improvements
#### Optimization #1:
**Keep track of a running sum instead of running `get_sum` in each iteration of the inner `end_idx` for loop**

In the brute solution, a lot of repetitive calculations are done in the inner `end_idx` for loop with the `get_sum` function. Instead of recalculating the sum from elements `start_idx` to `end_idx` in every iteration of the `end_idx` loop, we can store a `subarray_sum` variable to save calculations from previous iterations and simply add to it in each iteration of the `end_idx` loop.

```python
def min_sub_array_length(nums, sum):
    min_length = float("inf")
    for start_idx in range(len(nums)):
        subarray_sum = 0
        for end_idx in range(start_idx, len(nums)):
            subarray_sum += nums[end_idx]
            if subarray_sum >= sum:
                min_length = min(min_length, end_idx - start_idx + 1)
    return min_length if min_length != float("inf") else 0
```

This optimization reduces the time complexity from O(N<sup>3</sup>) to O(N<sup>2</sup>) with the addition of a variable to store the accumulating sum.


#### Optimization #2:
**Reduce number of calculations by terminating the inner `end_idx` for loop early**

With the improved solution, we can further reduce the number of iterations in the inner for loop by terminating it early. Once we have a `subarray_sum` that is equal to or greater than the target sum, we can simply move to the next iteration of the outer for loop. This is because the questions asks for minimum length subarray and any further iterations of the inner for loop would only cause an increase in the subarray length.

```python
def min_sub_array_length(nums, sum):
    min_length = float("inf")
    for start_idx in range(len(nums)):
        subarray_sum = 0
        for end_idx in range(start_idx, len(nums)):
            subarray_sum += nums[end_idx]
            if subarray_sum >= sum:
                min_length = min(min_length, end_idx - start_idx + 1)
                continue
    return min_length if min_length != float("inf") else 0
```

This is a minor time complexity improvement and this solution will still have a worst case runtime of O(n<sup>2</sup>). The improvement is nice, but to reduce the runtime from O(n<sup>2</sup>) to O(n), we would need to somehow eliminate the inner for loop.


## Solution #2: Two pointer approach
### Approach:

The optimal, two pointer approach to this problem utilizing the observations we made in the previous section. The main idea of this approach is that we grow and shrink an interval as we loop through the list, while keeping a running sum that we update as we alter the interval.

There will be two pointers, one to track the start of the interval and the other to track the end. They will both start at the beginning of the list and move dynamically to the right until they hit the end of the list.

First, we grow the interval to the right until it exceeds the minimum sum. Once we find that interval, we move the start pointer right as much as we can to shrink the interval until it sums to a number that is smaller than the target sum.

Then, we move the end pointer to once again to try and hit the sum with new intervals. If growing the interval by moving the end pointer leads to an interval that sums up to at least the target sum, we need to repeat the process of trying to shrink the interval again by moving the start pointer before further moving the end pointer.

As we utilize these two pointers to determine which intervals to evaluate, we have a variable to keep track of the current sum of the interval as we go along to avoid recalculating it every time one of the pointers moves to the right, and another variable to store the length of the shortest interval that sums up to >= the target sum.

This push and pull of the end and start pointer will continue until we finish looping through the list.

### Implementation
```python
def min_sub_array_length(nums, sum):
    start_idx = 0
    min_length, subarray_sum = float('inf'), 0

    for end_idx in range(len(nums)):
        subarray_sum += nums[end_idx]
        while subarray_sum >= sum:
            min_length = min(min_length, end_idx - start_idx + 1)
            subarray_sum -= nums[start_idx]
            start_idx += 1
    if min_length == float('inf'):
        return 0
    return min_length
```

### Time and space complexity
The time complexity of this solution is **O(n)** because each element is visited at most twice. In the worst case scenario, all elements will be visited once by the start pointer and another  time by the end pointer.

The space complexity would be **O(1)** because the solution doesn't create new data structures.

### Walkthrough
Take the example of `min_sub_array_length([2,3,1,2,4,3], 7)`. The left pointer starts at 0 and the right doesn't exist yet.

As we start looping through the list, our first interval is [2]. We won't fulfill the while loop condition until the list reaches [2, 3, 1, 2] whose sum, 8 is >= 7. We then set the `min_length` to 4.

Now, we shrink the interval to [3, 1, 2] by increasing `start_idx` by 1. This new interval sums up to less than the target sum, 7 so we need to grow the interval. In the next iteration, we grow the interval to [3, 1, 2, 4], which has a sum of 10 and once again, we satisfy the while loop condition.

We then shrink the interval to [1, 2, 4]. This is the shortest interval we've come across that sums up to at least the target sum, so we update the `min_length` to 3.

We now move the `end_idx` pointer and it hits the end of the list, with interval [2, 4, 3]. Then shrink the interval to [4, 3], which sums up to 7, the target sum. This is the shortest interval we've come across that sums up to at least the target sum, so we update the `min_length` to 2. This is the final result that is returned.

## Takeaways

This optimization can often be applied to improve solutions that involve the use of multiple for loops, as demonstrated in the example above. If you have an approach that utilizes multiple for loops, analyze the actions performed in those for loops to determine if repetitive calculations can be removed through strategic movements of multiple pointers.

**Note:** Though this walkthrough demonstrated applying the two pointer approach to an arrays problem, this approach is commonly utilized to solve string problems as well.
