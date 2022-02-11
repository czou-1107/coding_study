

class LinkedList:
    """ Doubly-linked list that points to both front and back """
    class Node:
        """ Node is implemented as a "private" class and contains all the
        data itself. It is an abstraction hidden from the user
        """
        def __init__(self, data, prev, next_):
            self.data = data
            self.prev = prev
            self.next = next_

        def __repr__(self):
            return f'{self.prev.data if self.prev is not None else "BGN"} - ' +\
                   f'{self.data} - ' +\
                   f'{self.next.data if self.next is not None else "END"}'


    def __init__(self):
        self.front = None
        self.back = None
        self.n_nodes = 0

    def __len__(self):
        return self.n_nodes

    def __repr__(self):
        if len(self) == 0:
            return '[]'
        node = self.front
        values = [node.data]
        while hasattr(node, 'next'):
            node = node.next
            if node is not None:
                values.append(node.data)
        return str(values)

    def debug(self):
        node = self.front
        print(node)
        while hasattr(node, 'next'):
            node = node.next
            print(node)


    def push_front(self, data):
        """ Add a node to the front of the linked list """
        # Create a new node with data
        new_node = self.Node(data, None, self.front)
        # If there was a previous front, change its pointers
        if self.front:
            self.front.prev = new_node
        # Assign new to front of list
        self.front = new_node

        self.n_nodes += 1


    def pop_front(self):
        """ Remove first node in linked list """
        node_to_pop = self.front
        if node_to_pop:  # Only act if the list isn't empty
            # front should now be the next node
            self.front = node_to_pop.next
            if self.front:  # Is not null pointer
                self.front.prev = None
        else:
            print('Nothing to pop!')

        self.n_nodes -= 1
