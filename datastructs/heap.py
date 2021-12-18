"""
Crude implementation of a heap

For an actual production-grade heap, check out heapq. Heapsort is easily
implemented as such:

```
from heapq import heappush, heappop

def heapsort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for i in range(len(h))]
```
"""
import sys


class CrudeHeap:
    """ A crude implementation of a heap, """
    def __init__(self):
        self.values = []
        self.n_values = 0


    def __getitem__(self, idx: int):
        # Just to make access easier
        return self.values[idx]


    @classmethod
    def heapify(cls, array: list):
        """ Instantiate a heap from an arbitrary array """
        instance = cls()
        for item in array:
            instance.push(item)
        return instance


    def _swap(self, i, j):
        self.values[i], self.values[j] = self.values[j], self.values[i]


    def _get_parent(self, idx: int) -> tuple:
        """ Get parent along with its index """
        parent_idx = idx // 2
        return self[parent_idx], parent_idx


    def _get_child(self, idx: int, which: str = 'priority'):
        """
        Get child, either 'left', 'right', or 'priority' along with its index

        With 'left' or 'right', a childfree parent will raise IndexError, while
        with 'priority' it will return (None, None)
        """
        if which == 'left':
            child_idx = 2 * idx + 1
        elif which == 'right':
            child_idx = 2 * idx + 2
        elif which == 'priority':
            left = right = sys.maxsize
            try:
                left, left_idx = self._get_child(idx, 'left')
            except IndexError:
                pass

            try:
                right, right_idx = self._get_child(idx, 'right')
            except IndexError:
                pass

            if left == sys.maxsize and right == sys.maxsize:
                return None, None

            if left < right:
                child_idx = left_idx
            else:
                child_idx = right_idx
        else:
            raise ValueError('which is not recognized.')

        return self[child_idx], child_idx


    def _verify_heap_order_priority(self, _idx: int = 0):
        """ Recursively verify that heap order priority is satisfied """
        try:
            left, left_idx = self._get_child(_idx, 'left')
        except IndexError:  # There are no left children to check
            pass
        else:  # Check its child and recurse
            assert self[_idx] <= left, \
                f'Failed check at index {_idx} (left): {self[_idx]} > {left}'
            self._verify_heap_order_priority(left_idx)

        try:
            right, right_idx = self._get_child(_idx, 'right')
        except IndexError:
            pass
        else:
            assert self[_idx] <= right, \
                f'Failed check at index {_idx} (right): {self[_idx]} > {right}'
            self._verify_heap_order_priority(right_idx)


    def push(self, value):
        """ Push a value into heap """
        # Initialize new value at bottom of heap
        self.values.append(value)
        self.n_values += 1

        # Percolate upward until it reaches proper position
        current_idx = self.n_values - 1
        parent, parent_idx = self._get_parent(current_idx)
        while self[current_idx] < parent and current_idx > 0:
            self._swap(current_idx, parent_idx)
            current_idx = parent_idx
            parent, parent_idx = self._get_parent(current_idx)

        # This extra check is just there as sanity check
        self._verify_heap_order_priority()


    def pop(self):
        """ Pop the lowest priority item (at root) """
        # Always returns root, but this now creates inconsistency!
        self._swap(0, self.n_values - 1)
        # A cute advantage here is that since we use list (with O(n) pop at index 0),
        # the swap actually allows us to instead do an O(1) pop at index -1
        root = self.values.pop(-1)
        self.n_values -= 1

        # Percolate the new root downward until it reaches proper position
        current_idx = 0
        child, child_idx = self._get_child(current_idx, 'priority')
        while child is not None and self[current_idx] > child:
            self._swap(current_idx, child_idx)
            current_idx = child_idx
            child, child_idx = self._get_child(current_idx, 'priority')

        self._verify_heap_order_priority()
        return root
