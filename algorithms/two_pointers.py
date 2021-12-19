"""
A set of problems utilizing a "two pointers" technique, which work under monotonicity:
a pointer always moves in a certain direction

Within this class there are two basic solution types: equi-directional (both
arrays start at one end) and opposite-directional (opposite ends and termination
condition is when they meet)
"""
import sys


def minimum_subarray_with_given_product(array: list, p: int) -> int:
    """ Given array, find length of minimum subarray with product >= p

    Solution is in O(n). The key is that if we find the minimum subarray starting
    at i (and say it terminates at j), then we know that the solution for minimum
    subarray starting at i+1 *must* terminate *after* j, which satisfies monotonicity!
    """
    n = len(array)

    cur_product = 1
    min_size = sys.maxsize

    i = j = 0  # Equi-directional
    while i < n:  # Termination condition: end of array for pointer i
        # Solve for minimum subarray *beginning* at i
        while j < n and cur_product < p:
            # Only enter this block (incrementing j) *if* cur_product is smaller than p
            # Otherwise, you want to keep incrementing i (and decreasing cur_product)
            # until you are once again below
            cur_product *= array[j]
            j += 1

            if j == n and cur_product < p:
                # Add some validation for unreasonable p's
                raise ValueError('p is unsatisfiable given array!')

        if cur_product >= p:
            min_size = min(min_size, j - i)

        cur_product /= array[i]
        i += 1

    return min_size


def find_exact_pairwise_sum(array: list, s: sum) -> tuple:
    """ Given sorted array, find elements that sum to exactly s (if they exist) """
    n = len(array)

    i, j = 0, n - 1

    while i < j:
        current_sum = array[i] + array[j]
        if current_sum == s:
            return array[i], array[j]

        if current_sum > s:  # Need to decrement
            j -= 1
        elif current_sum < s:  # Need to increment
            i += 1
    return None


def longest_mountain_subarray(array: list) -> int:
    """ Given an array, return length of longest "mountain" subarray

    A mountain subarray is one composed of strictly increasing values followed
    by strictly decreasing values
    """


def zero_sum_triplets(array: list) -> list:
    """ Given an array, return all distinct triplets that sum to zero """


def remove_consecutive_duplicates_string(string: str) -> str:
    """ Remove consecutive duplicates """