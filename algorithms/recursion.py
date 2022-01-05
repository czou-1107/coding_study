"""
Some problems that can be solved using recursion
"""
try:
    import numpy as np
    _numpy_available = True
except ImportError:
    print('numpy not detected in environment. Some solutions will fail to run!')
    _numpy_available = False


def tower_of_hanoi(n: int, source: int = 'source', dest: int = 'dest', aux: int = 'aux'):
    """ See https://en.wikipedia.org/wiki/Tower_of_Hanoi

    This solution has O(2^n) complexity """
    if n == 1:
        return [(1, source, dest)]
    # The starting state has the entire current stack at source, aux is empty,
    # and everything in dest is, by construction, larger than anything left.

    # Move stack so that bottommost ring can be placed in terminal destination
    stack_to_aux = tower_of_hanoi(n-1, source, aux, dest)
    intermediate_step = (n, source, dest)
    # Swap labels of source and aux, and recurse
    stack_to_dest = tower_of_hanoi(n-1, aux, dest, source)
    return [*stack_to_aux, intermediate_step, *stack_to_dest]


class TowerOfHanoi:
    """ Representation of states in solving tower_of_hanoi

    Validates each step, used for testing """
    def __init__(self, n: int):
        self.n = n
        self._reset()

    def _reset(self):
        self.state = {
            'source': [self.n - i for i in range(self.n)],  # 1-based index
            'aux': [],
            'dest': [],
        }

    def __repr__(self):
        return repr(self.state)

    def move(self, step: tuple):
        """ Step is instruction of form (ring, from, to) """
        ring, from_, to_ = step

        assert self.state[from_], 'Trying to move from empty stack'
        topmost = self.state[from_][-1]
        if topmost != ring:
            if ring in self.state[from_]:
                raise AssertionError('Trying to move non-topmost ring')
            else:
                raise AssertionError('Trying to move ring not in stack')
        assert len(self.state[to_]) == 0 or ring < self.state[to_][-1], \
            'Trying to move ring to smaller dest'

        self.state[to_].append(self.state[from_].pop())

    def evaluate(self, verbose=True):
        steps = tower_of_hanoi(self.n)
        if verbose:
            print(self)
        for step in steps:
            self.move(step)
            if verbose:
                print(self)
        # Check for correctness:
        if self.state['dest'] == [self.n - i for i in range(self.n)]:
            if verbose:
                print('Success!')
            return True
        else:
            return False


def family_structure_with_deterministic_children(n: int, k: int):
    """ Determine gender of k-th child in n-th generation

    Setup: all parents spawn exact 2 children with the same timing, e.g.
    child 1 at age A1 and child 2 at age A2. (M)ales spawn (M, F) and (F)emales
    spawn (F, M)
    """
    if n == 1:
        return 'M'
    # We know that parent is (k // 2)-th child of previous generation
    parent_k = (k + 1) // 2  # ensure 1-based index
    child_nbr = 1 if k % 2 == 1 else 2  # 1-based index
    parent_gender = family_structure_with_deterministic_children(n-1, parent_k)

    if (parent_gender == 'M' and child_nbr == 1) or (parent_gender == 'F' and child_nbr == 2):
        return 'M'
    return 'F'


class MinCostPath:
    """ Various implementations of a minimum-cost path for matrix traversal

    Given a matrix :costs: of shape (m, n) the goal is to traverse from (0, 0) (top-left)
    to (m-1, n-1) (bottom right) and moving through (i, j) costs the corresponding value

    See also: Levenshtein distance
    """
    def __init__(self, costs, allow_diagonal_move: bool = True):
        if isinstance(costs, list):
            costs = np.array(costs)

        self.costs = costs
        self.allow_diagonal_move = allow_diagonal_move

        self._max_cost = np.inf


    def solve_recursive(self, m=None, n=None):
        """ Naive solution with exponential complexity (3^n if diagonal allowed else 2^n)
        """
        if m is None and n is None:  # Main entrypoint
            m = self.costs.shape[0] - 1
            n = self.costs.shape[1] - 1

        if m == 0 and n == 0:  # Base case
            return self.costs[m, n]
        if m < 0 or n < 0:  # Out-of-bounds
            return self._max_cost

        return self.costs[m, n] + min(
            self.solve_recursive(m-1, n),  # Move 1 up
            self.solve_recursive(m, n-1),  # Move 1 left
            # Check diagonal move if allowed. Otherwise set it to out-of-bounds
            self.solve_recursive(m-1, n-1) if self.allow_diagonal_move else self._max_cost,
        )


    def solve_memoize(self, m=None, n=None):
        if m is None and n is None:  # Main entrypoint
            m = self.costs.shape[0] - 1
            n = self.costs.shape[1] - 1
            # Assume that all distances are non-negative, so we can simply check if
            # cache = -1 (another method is to just use dict keys)
            self._costs_from_origin = -np.ones_like(self.costs)
            self._costs_from_origin[0, 0] = self.costs[0, 0]  # Base case

        if m < 0 or n < 0:  # Out-of-bounds
            return self._max_cost
        if self._costs_from_origin[m, n] != -1:  # Has been computed previously
            return self._costs_from_origin[m, n]

        current_cost = self.costs[m, n] + min(
            self.solve_memoize(m-1, n),  # Move 1 up
            self.solve_memoize(m, n-1),  # Move 1 left
            # Check diagonal move if allowed. Otherwise set it to out-of-bounds
            self.solve_memoize(m-1, n-1) if self.allow_diagonal_move else self._max_cost,
        )
        self._costs_from_origin[m, n] = current_cost
        return current_cost


    def solve_dp(self):
        # This is technically the same as memoization, but constructs the cost from origin
        # matrix directly (in a "bottom-up" vs "top-down") approach
        # Using this approach it is easy to see complexity is reduced to O(mn)
        costs_from_origin = np.zeros_like(self.costs)
        costs_from_origin[0, 0] = self.costs[0, 0]  # Base case

        # Fill the first row and column with allowed movement costs (e.g. straight down/right)
        for i in range(1, self.costs.shape[0]):
            costs_from_origin[i, 0] = costs_from_origin[i-1, 0] + self.costs[i, 0]
        for j in range(1, self.costs.shape[1]):
            costs_from_origin[0, j] = costs_from_origin[0, j-1] + self.costs[0, j]

        # Fill rest of the array
        for i in range(1, self.costs.shape[0]):
            for j in range(1, self.costs.shape[1]):
                costs_from_origin[i, j] = self.costs[i, j] + min(
                    costs_from_origin[i-1, j],
                    costs_from_origin[i, j-1],
                    costs_from_origin[i-1, j-1] if self.allow_diagonal_move else self._max_cost,
                )

        return costs_from_origin[-1, -1]
