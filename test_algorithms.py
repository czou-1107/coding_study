import sys
import pytest

from algorithms import max_subarray
from algorithms import sorting
from algorithms import dutch_national_flag
from algorithms import two_pointers
from algorithms import fibonacci
from algorithms import recursion
from algorithms import sliding_window
from algorithms import dp


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


@pytest.mark.parametrize('array, p, expect', [
    ([1, 2, 3, 4, 5, 6], 20, 2),
    ([1, 2, 3, 4, 5, 6], 35, 3),
])
def test_minimum_subarray_with_given_product(array, p, expect):
    assert two_pointers.minimum_subarray_with_given_product(array, p) == expect


def test_minimum_subarray_with_given_product_raises():
    with pytest.raises(ValueError):
        two_pointers.minimum_subarray_with_given_product([1, 2, 3, 4, 5, 6], 1000)


@pytest.mark.parametrize('array, s, expect', [
    ([1, 2, 3, 4, 6], 9, (3, 6)),
    ([0, 2, 4, 5, 8, 12], 7, (2, 5)),
    ([0, 1, 6, 8, 9], 5, None),
])
def test_exact_pairwise_sum(array, s, expect):
    assert two_pointers.find_exact_pairwise_sum(array, s) == expect


@pytest.mark.parametrize('fn', [
    fibonacci.fibonacci_recursion,
    fibonacci.fibonacci_memoized,
    fibonacci.fibonacci_exact,
])
@pytest.mark.parametrize('n,expect', [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (10, 55),
    (20, 6765),
])
def test_fibonacci(fn, n, expect):
    assert fn(n) == expect


@pytest.mark.parametrize('n', [1, 2, 3, 4, 10])
def test_tower_of_hanoi(n):
    assert recursion.TowerOfHanoi(n).evaluate(verbose=False)


@pytest.mark.parametrize('n,k,expect', [
    (1, 1, 'M'),
    (2, 1, 'M'),
    (2, 2, 'F'),
    (3, 3, 'F'),
    (4, 3, 'F'),
    (4, 6, 'M')
])
def test_family_structure_with_deterministic_children(n, k, expect):
    assert recursion.family_structure_with_deterministic_children(n, k) == expect


@pytest.mark.parametrize('array,s,expect', [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 9, [2, 3, 4]),
    ([3, 1, 6, 4, 5], 9, [4, 5]),
    ([3, 1, 6, 4, 10], 9, []),
])
def test_subarray_sum_equals(array, s, expect):
    assert sliding_window.subarray_sum_equals(array, s) == expect


@pytest.mark.parametrize('array,k,expect', [
    ([1, 2, 2, 1, 2, 1], 3, -1),
    ([1, 2, 2, 1, 2, 1], 2, 2),
    ([1, 1, 1, 2, 2, 3, 3, 2], 3, 4),
    ([1, 1, 1, 2, 2, 3, 3, 2, 1], 3, 3),
])
def test_subarray_sum_equals(array, k, expect):
    assert sliding_window.smallest_subarray_with_k_distinct(array, k) == expect


@pytest.mark.parametrize('array,expect', [
    ([-7, 1, 5, 2, -4, 3, 0], [3, 6]),
    ([-2, 1, 9, 2, -6, 3, 0], [2]),
    ([1, 2, 3, 4, 5], []),
])
def test_equilibrium_indices(array, expect):
    assert sliding_window.equilibrium_indices(array) == expect


@pytest.mark.parametrize('array,expect', [
    ([[3, 4, 1, 2], [2, 1, 8, 9], [4, 7, 8, 1]], 13)
])
@pytest.mark.parametrize('solution_method', [
    'solve_recursive', 'solve_memoize', 'solve_dp'
])
def test_min_cost_path(array, solution_method, expect):
    solver = recursion.MinCostPath(array, allow_diagonal_move=True)
    solution = getattr(solver, solution_method)()
    assert solution == expect


@pytest.mark.parametrize('array,expect', [
    ([10, 2, 1, 8, 1, 3], 57),
])
def test_minimum_cost_of_reducing_array(array, expect):
    assert dp.minimum_cost_of_reducing_array(array) == expect


@pytest.mark.parametrize('string,pat,expect', [
    ('abcde', 'ab?de', True),
    ('abcde', 'abc', False),
    ('abcde', '*', True),
    ('abcde', 'ab*e', True),
    ('abcde', '*f', False),
    ('abcde', '????e', True),
    ('abcde', '???', False),
])
def test_me(string, pat, expect):
    assert dp.wildcard_matching(string, pat) == expect