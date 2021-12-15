"""
Given an array with several distinct elements (e.g. 0, 1, 2), sort the elements
(in O(n) time)
"""

def _swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def two_pass(array: list) -> list:
    """ This effectively uses an insertion sort where insert costs O(1) b/c
    we are only sorting 1 unique value at a time

    To sort N unique values, you would need N-1 passes, each taking O(N) time
    """
    array = array.copy()
    n = len(array)

    # First pass: sort 0's
    end_0 = 0
    for i in range(n):
        if array[i] == 0:
            _swap(array, i, end_0)
            end_0 += 1

    # Second pass: sort 1's
    end_1 = end_0
    for i in range(end_0, n):
        if array[i] == 1:
            _swap(array, i, end_1)
            end_1 += 1

    return array


def three_way_partition(array: list) -> list:
    """ This only requires a single pass, and is more efficient

    A 3-way partition can actually be used to make quicksort more efficient
    (moving from O(log_2 n) to O(log_3 n) """
    array = array.copy()
    n = len(array)

    low = mid = 0
    high = n - 1

    while mid <= high:
        if array[mid] == 0:
            _swap(array, mid, low)
            mid += 1
            low += 1
        elif array[mid] == 1:
            mid += 1
        elif array[mid] == 2:
            _swap(array, mid, high)
            high -= 1
    return array


def brute_force(array: list) -> list:
    """ YOLO
    """
    counts = {0: 0, 1: 0, 2: 0}  # Should probably use collections.Counter
    for el in array:
        counts[el] += 1

    new_array = []
    for k, cnt in counts.items():
        for el in range(cnt):
            new_array.append(k)
    return new_array