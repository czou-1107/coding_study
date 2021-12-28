"""
Some problems that can be solved using recursion
"""


def tower_of_hanoi(n: int, source: int = 'source', dest: int = 'dest', aux: int = 'aux'):
    """ See https://en.wikipedia.org/wiki/Tower_of_Hanoi

    This solution has O(2^n) complexity """
    if n == 1:
        return [(1, source, dest)]
    stack_to_aux = tower_of_hanoi(n-1, source, aux, dest)
    intermediate_step = (n, source, dest)
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
    child_nbr = (k % 2) + 1  # 1-based index

    parent_gender = family_structure_with_deterministic_children(n-1, k // 2)
    if (parent_gender == 'M' and child_nbr == 1) or (parent_gender == 'F' and child_nbr == 2):
        return 'M'
    else:
        return 'F'
