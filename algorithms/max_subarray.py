"""
Maximum subarray: given an array, find the maximum sum from any subarray

Problem tags: dynamic programming
"""
import sys


def kadane(arr: list) -> int:
    """ Solve maximum subarray in O(n)

    Key here is to consider that if you know the local max at any array position,
    you don't need to recompute it to get local max of next position:
    
    If the next position is >0, then the new local max is just += next value
    """
    local_max = 0
    global_max = -sys.maxsize  # Technically it can get lower, but it would take
                               # a very pathological example to make this wrong
    for val in arr:
        local_max = max(val, val + local_max)
        if local_max > global_max:
            global_max = local_max

    return global_max


def flip_bits(arr: list) -> int:
    """ Given binary array, return maximum run of 1's obtainable by flipping
    any contiguous sub-array a single time """
    # TODO


def maximum_subarray_with_concatenation(arr: list, k: int) -> int:
    """ Maximum subarray but with concatenating arr k times """
    # TODO


def maximum_submatrix(mat: list) -> int:
    """ Largest submatrix on a matrix """
    # TODO
