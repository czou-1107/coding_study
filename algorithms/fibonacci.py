"""
Various implementations of Fibonacci
"""
import math
from functools import wraps


def fibonacci_recursion(n: int, /) -> int:
    """ Compute values recursively.

    Very inefficient: time complexity of O(2^n) """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursion(n - 1) + fibonacci_recursion(n - 2)


def _memoize(f):
    # A built-in solution would be functools.lru_cache, which also limits cache size
    # memoizing fibonacci reduces complexity to O(n)
    # This implementation is a "top-down" DP approach, where the call stack is produced
    # from n to 1
    cache = {}

    @wraps(f)
    def wrapped(*args):
        if args in cache:
            return cache[args]
        result = f(*args)
        cache[args] = result
        return result

    return wrapped


fibonacci_memoized = _memoize(fibonacci_recursion)


_phi = (1 + math.sqrt(5)) / 2


def fibonacci_exact(n: int) -> int:
    """ A closed-from expression is available, known as Binet's formula

    See derivation at: https://en.wikipedia.org/wiki/Fibonacci_number#Matrix_form
    """
    return int( (_phi ** n - (-_phi) ** -n) / math.sqrt(5) )
