import sys
import pytest

from algorithms import max_subarray
from algorithms import sorting
from algorithms import dutch_national_flag


@pytest.mark.parametrize('array,max_sum', [
    ([-1, 2, -2, 5, 7, -3, 1], 12),  # sample from website
    ([-15, -5, -7, -2], -2),  # all negatives
    ([1, 2, 5, 0, 10], 18),  # all positives
])
def test_kadane(array, max_sum):
    assert max_subarray.kadane(array) == max_sum


@pytest.mark.parametrize('array', [
    [5, 1, 3, 4, 2, 7],
    [5, 4, 3, 2, 1, 5],
    [0, 0, 0, 0, 0],
])
def test_quicksort_partition(array):
    partition_index = sorting._partition(array, 0, len(array) - 1)
    assert max(array[ : partition_index], default=-sys.maxsize) <= array[partition_index]
    assert min(array[partition_index + 1: ], default=sys.maxsize) >= array[partition_index]


@pytest.mark.parametrize('sort_fn', [
    sorting.bubble_sort,
    sorting.selection_sort,
    sorting.insertion_sort,
    sorting.quick_sort,
    sorting.merge_sort,
    sorting.heap_sort,  # TODO: test heap.py. This working is basically an integration test
])
@pytest.mark.parametrize('array', [
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [1, 3, 5, -1, 2, 0],
    [0, 0, 3, -5, -10, -12, 0],
    [5, 1, 2, 3, 4, 5],
    [1, 1, 1, 1, 1],
])
def test_sorting(sort_fn, array):
    assert sorted(array) == sort_fn(array)


@pytest.mark.parametrize('array', [
    [0, 0, 1, 1, 2, 2],
    [0, 1, 2, 0, 1, 2],
])
@pytest.mark.parametrize('sort_fn', [
    dutch_national_flag.two_pass,
    dutch_national_flag.three_way_partition,
    dutch_national_flag.brute_force,
])
def test_dutch_national_flag(sort_fn, array):
    assert sorted(array) == sort_fn(array)