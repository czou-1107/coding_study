"""
Set of problems utilizing a technique for finding subarrays satisfying given
conditions. Typically they fall in two types:

- Fixed window, e.g. max sum subarray of size k
- Variable window, e.g. maximum subarray
"""


def subarray_sum_equals(array: list, s: int) -> list:
    """ Find a subarray with sum equal to s

    Sliding window allows computation in O(n) vs O(n^2) by skipping repeat computations
    """
    # TODO: is there maybe a solution using deque?
    n = len(array)
    curr_sum = array[0]
    window_start = 0
    window_end = 1

    # Iterate through window end pointer, sliding the window start pointer as needed
    # The end pointer is responsible for appending new items, while the start pointer
    # is responsible for culling old ones
    while window_end <= n:
        # If curr_sum exceeds s, then keep removing start points until it's below again
        while curr_sum > s and window_start < window_end:
            curr_sum -= array[window_start]
            window_start += 1

        if curr_sum == s:
            return array[window_start: window_end]

        # Update current sum--but only if window_end is still a valid index!
        if window_end < n:
            curr_sum += array[window_end]

        window_end += 1
    return []  # No valid subarray found


def smallest_subarray_with_k_distinct(array: list, k: int) -> list:
    """ Find smallest subarray containing K distinct elements """
    n = len(array)
    smallest_subarray_size = n + 1

    n_distinct = 0
    window_start = window_end = 0
    curr_distincts = {}

    # Invariant that is maintained each iteration:
    # Contains the smallest subarray (if possible) that ends in window_end and contains
    # k distinct elements
    while window_end < n:
        # Append next item, and update current subarray statistics
        if array[window_end] in curr_distincts:
            curr_distincts[array[window_end]] += 1
        else:
            curr_distincts[array[window_end]] = 1
            n_distinct += 1

        # If we have enough distincts, try and cull (increment start counter)
        # This maintains our invariant. Note: we cull under one of two conditions:
        # 1. If we have > k distinct, cull down until k distinct
        # 2. If we have = k distinct, cull IF it is a duplicate
        while window_start < window_end and (
            n_distinct > k or (
                n_distinct == k and curr_distincts[array[window_start]] > 1
            )
        ):
            curr_distincts[array[window_start]] -= 1
            if curr_distincts[array[window_start]] == 0:
                n_distinct -= 1
            window_start += 1

        # Check if this subarray is smallest
        if n_distinct == k:
            smallest_subarray_size = min(smallest_subarray_size, window_end - window_start + 1)

        window_end += 1

    if smallest_subarray_size > n:  # Not possible, array doesn't have enough values
        return -1
    return smallest_subarray_size


def equilibrium_indices(array: list) -> list:
    """ Find all equilibrium indices of an array

    An equilibrium index is defined as i s.t. sum(array[:i]) == sum(array[i+1:])
    """
    # Bit of a hack here, but the initialization + the loop (where left_sum is first
    # incremented before comparison, and right_sum is decremented *after* comparison),
    # means we are properly comparing array[:i] to array[i+1:]
    right_sum = sum(array[1:])
    left_sum = -array[0]

    indices = []
    for i in range(len(array)):
        left_sum += array[i]
        if left_sum == right_sum:
            indices.append(i)
        right_sum -= array[i]
    return indices


def count_distinct_element_in_k_size_window(array: list, k: int) -> list:
    """ Given an array, count number of distinct elements in a sliding window of size k
    """
    # TODO


def substring_anagrams(string: str, substring: str) -> list:
    """ Given string and substring, return all indices of string that are anagrams of substring

    For example, if string is "subbusbam", and substring is "sub", then indices
    are at 0, 3, 4 """
    # TODO