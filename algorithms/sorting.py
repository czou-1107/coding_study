"""
Sorting algorithms
"""
from __future__ import annotations

import sys


def _swap(arr: list, i: int, j: int):
    # Python allows assignment without needing to explicitly create temp variable
    arr[i], arr[j] = arr[j], arr[i]


def _get_min(arr: list) -> tuple[int, int]:
    # Return (min :arr:, idxmin :arr:)
    current_min = sys.maxsize
    current_min_idx = -1
    for i, el in enumerate(arr):  # Could also iterate over range(arr)
        if el < current_min:
            current_min = el
            current_min_idx = i
    return current_min, current_min_idx


def bubble_sort(array: list[int]) -> list[int]:
    """ Continuously swap adjacent elements that are in wrong order, so that
    largest items "bubble" up to the right

    Worst complexity: O(n^2)
    Avg complexity: O(n^2)
    Best complexity: O(n) <- but not the way this is currently implemented!
    Space complexity: O(1)
    Stable: yes

    Notes: O(n^2) sort, since it takes O(n) to sort each element """
    array = array.copy()
    n = len(array)

    for i in range(n):
        # At this point, all elements to the *right* are sorted
        # Iteratively swap larger item right
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                _swap(array, j, j + 1)
    return array


def selection_sort(array: list[int]) -> list[int]:
    """ Repeatedly extract minimum in unsorted subarray and append to sorted array

    Worst complexity: O(n^2)
    Avg complexity: O(n^2)
    Best complexity: O(n^2) <- need to find min even if array is perfected sorted
    Space complexity: O(1)
    Stable: no
    """
    unsorted = array.copy()
    sorted = []

    while unsorted:
        _, next_min_idx = _get_min(unsorted)
        sorted.append(unsorted.pop(next_min_idx))
    return sorted


def insertion_sort(array: list[int]) -> list[int]:
    """ Repeatedly insert next item in correct place (in sorted array)

    Worst complexity: O(n^2)
    Avg complexity: O(n^2)
    Best complexity: O(n) <- with the short circuit
    Space complexity: O(1)
    Stable: yes
    """
    array = array.copy()
    n = len(array)

    for i in range(n):
        # All points to *left* are sorted, and we must determine which position
        # to insert next item into
        for j in range(0, i):
            if array[j] > array[i]:
                _swap(array, i, j)
            # An optimization here is to short-circuit inner loop ASAP:
            else:
                continue
    return array


def _partition(arr, low, high):
    # Find a pivot such that everything to its left is < and right is > than it
    # There are many ways to partition. Ideally, the pivot should be median

    # This implementation follows Hoare's algorithm, choosing pivot as leftmost index
    # Robustness can be improved using random pivot, median-of-3
    pivot_index = low
    pivot = arr[pivot_index]

    while low < high:
        # Need to add low <= high condition so not to crash if pivot is max
        while low <= high and arr[low] <= pivot:
            low += 1
        while arr[high] > pivot:
            high -= 1

        if low < high:
            _swap(arr, low, high)
    _swap(arr, high, pivot_index)  # Puts pivot in correct place when left and right are correct
    return high


def quick_sort(array: list[int], low: int = None, high: int = None) -> list[int]:
    """ Divide & conquer #1

    The key is to partition array using a pivot value, such that left partition
    contains only those smaller and right only those larger and recurse

    Worst complexity: O(n^2) <-- e.g. array almost sorted and pivot is first/last; all duplicates
    Avg complexity: O(n log n)
    Best complexity: O(n log n)
    Space complexity: O(n log n)
    Stable: no

    An improvement is apparently to use three-way partition (Dutch National Flag)
    Re: time complexity. Note that worst complexity occurs when the recurrence is:

    T(n) = T(m) + T(n-m) + theta(n), theta(n) is partition complexity, for small m

    Even if you can achieve partition of something like T(p * n) + T((1-p) * n),
    for large p, this will still be O(n log n)
    """
    is_initial_call = False
    if low is None and high is None:
        is_initial_call = True
        array = array.copy()
        low = 0
        high = len(array) - 1  # This is used to access index, so it must be n-1!

    if low < high:
        partition_index = _partition(array, low, high)

        quick_sort(array, low, partition_index - 1)
        quick_sort(array, partition_index + 1, high)

    if is_initial_call:
        return array


def _merge(left, right):
    left_idx = 0
    right_idx = 0

    n_left = len(left)
    n_right = len(right)

    sorted = []
    while left_idx < n_left and right_idx < n_right:
        if left[left_idx] <= right[right_idx]:
            sorted.append(left[left_idx])
            left_idx += 1
        else:
            sorted.append(right[right_idx])
            right_idx += 1

    # Once one set of indices is exhausted, just append everything else
    if left_idx < n_left:
        for i in range(left_idx, n_left):
            sorted.append(left[i])
    else:
        for i in range(right_idx, n_right):
            sorted.append(right[i])

    return sorted


def merge_sort(array: list[int]) -> list[int]:
    """ Divide & conquer #2

    Recursively split array into halves, sort the halves, and then merge the
    halves together. The base case is just a singleton

    Worst complexity: O(n log n)
    Avg complexity: O(n log n)
    Best complexity: O(n log n)
    Space complexity: O(n)
    Stable: yes

    Python's default sort (TimSort) uses a hybrid of merge and insertion sort
    It is useful in external sorting because arrays are accessed sequentially
    """
    array = array.copy()
    n = len(array)

    if n == 1:
        return array

    left_array = array[ : n // 2]
    right_array = array[n // 2 : ]
    return _merge(merge_sort(left_array), merge_sort(right_array))


def heap_sort(array: list[int]) -> list[int]:
    """ Use a heap data structure (see heap.py module for implementation)

    Worst complexity: O(n log n)
    Avg complexity: O(n log n)
    Best complexity: O(n log n)
    Space complexity: O(1)
    Stable: no
    """
    # HACK: Don't let broken code here break entire module :(
    from datastructs.heap import CrudeHeap

    heap = CrudeHeap.heapify(array)
    return [heap.pop() for _ in array]
