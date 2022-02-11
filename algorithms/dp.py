"""
Dynamic programming problems
"""
# TODO: write tests for these modules
import sys


class MaximumSumNonOverlappingArray:
    def __init__(self, array: list, k: int):
        """ Find two non-overlapping subarrays, each of size k, with the max sum
        """
        self.array = array
        self.k = k
        self.n = len(array)


    def base(self):
        # Naive O(n^2 solution)
        # Short-circuiting conditions:
        if self.n == 2 * self.k:
            return sum(self.array)
        if self.n < 2 * self.k:
            return None

        max_sum = -sys.maxsize
        for i in range(self.n):
            for j in range(i + self.k, self.n):
                current_sum = sum(self.array[i:i+self.k]) + sum(self.array[j:j+self.k])
                max_sum = max(current_sum, max_sum)
        return max_sum


    def optimized(self):
        # Optimized O(n) solution
        # Keep same short-circuiting conditions:
        if self.n == 2 * self.k:
            return sum(self.array)
        if self.n < 2 * self.k:
            return None

        max_sum = -sys.maxsize
        # Idea: work is duplicated since we are taking max over smaller and smaller
        # subarray in the inner loop. Why not record the max subarray starting from j?

        # Compute max subarray starting from j, indexed to correspond with original array
        # This should take O(n) time
        max_starting_from_j = [0] * (self.n - self.k + 1)
        max_starting_from_j.append(-1)  # Enable first comparison
        for j in reversed(range(self.k, self.n - self.k + 1)):
            right_sum = sum(self.array[j: j + self.k])
            max_starting_from_j[j] = max(max_starting_from_j[j + 1], right_sum)

        # Now iterate over k-sized subarrays from the left. For each iteration, finding
        # the optimal right subarray sum is just a lookup. This runs in O(n) also
        for i in range(self.n - 2*self.k + 1):
            left_sum = sum(self.array[i:i+self.k])
            best_right_sum = max_starting_from_j[i+self.k]
            max_sum = max(max_sum, left_sum + best_right_sum)

        return max_sum


def minimum_cost_of_reducing_array(array: list) -> int:
    """ Given an array A, the merge operation is defined between adjacent elements
    (A[i], A[i+1]) costs A[i] + A[i+1] and subsitutes the pair with the sum

    Determine the minimum cost to merge A to size 1

    Note: greedy approach will **not** work!
    """
    # Naive solution uses recursion
    # TODO: figure out solution in non-exponential time!
    n = len(array)
    if n == 2:
        return array[0] + array[1]

    # Find minimum cost of reducing each element:
    best_split_cost = sys.maxsize
    for i in range(n - 1):
        # Merging i with i + 1
        merged_element = array[i] + array[i+1]
        merged = [*array[:i], merged_element, *array[i+2:]]

        remaining_cost = minimum_cost_of_reducing_array(merged)
        cost_i = merged_element + remaining_cost
        best_split_cost = min(best_split_cost, cost_i)
    return best_split_cost


def minimum_removals_to_diff_condition(array: list, k: int):
    """ Determine the minimum number of elements to remove from array such that
    the max difference between remaining elements <= k
    """
    # O(n log n) solution: sort then iteratively remove
    n = len(array)  # Assume array is sorted for now
    # array = sorted(array)  # O(n log n)

    # # Base case:
    # if array[-1] - array[0] <= k:
    #     return 0

    # # If condition is not reached, then you have to remove something. Use
    # # recursion to determine which one to remove
    # return 1 + min(minimum_removals_to_diff_condition(array[1:], k),
    #                minimum_removals_to_diff_condition(array[:-1], k))


    # The recursive technique's drawback is that it repeatedly computes diffs.
    # We can do this in O(n):
    print([f'{i:02d}' for i in range(n)])
    print([f'{i:02d}' for i in array])
    j = 0
    largest_array_size = -1
    for i in range(n):
        while array[j] - array[i] <= k and j < n - 1:
            j += 1
        print(f'For {i=}, largest {j=}. Array size={j - i - 1}')
        largest_array_size = max(largest_array_size, j - i + 1)
        # Find largest index that satisfies the condition
    return n - largest_array_size + 1


def wildcard_matching(string: str, pat: str) -> bool:
    """ Wildcard matching with '?' and '*', and a base dictionary a-z (lower)

    This is globbing, where '?' matches any single character and '*' matches all
    """
    # Try using recursion
    print(string, pat)
    s, p = len(string), len(pat)

    if p == 1 and s == 1:
        return string == pat
    if p == 1:  # s > 1
        return pat == '*' and wildcard_matching(string[:-1], pat)
    if s == 1:  # p > 1
        return False

    if string[-1] == pat[-1] or pat[-1] == '?':
        return wildcard_matching(string[:-1], pat[:-1])
    if pat[0] == '*':
        return wildcard_matching(string[:-1], pat) or wildcard_matching(string, pat[:-1])
    return False
