"""Created by Byebrid. hamilton() will definitely not necessarily find shortest
path. This means this script can be used to provide an upper bound but not find
the smallest possible superpermutation for any sets of size > 4.
"""

from itertools import permutations

string = 'ABCDEF'

# Setting up array of all permutations of string
perms = [''.join(p) for p in permutations(string)]


class Node:
    """A Node is some permutation of the desired letters."""

    def __init__(self, value):
        self.value = value
        self.childs = set([])

    def __repr__(self):
        return "Node:" + self.value

    def find_childs(self, group):
        """Adds tuple of (child, weight) for each other node in the list of
        nodes.
        """
        self.childs = set([])
        for other in group:
            if other == self:
                continue
            for index in range(len(self.value)):
                # If last portion of self is same as beginning of other:
                if self.value[index] == other.value[0] and self.value[index:] in other.value:
                    # Append the Node object and index (which = the 'distance')
                    self.childs.add((other, index))


# Create all 'words' as Node objects
nodes = [Node(p) for p in perms]


def hamilton(group, pt, path=[]):
    """group is constantly updated as visited nodes are removed from group."""
    # print("\ngroup = {}, pt = {}, path = {}".format(group, pt, path))
    path.append(pt)
    # If last element of group has been reached, return path.
    if len(group) == 1:
        return path
    pt.find_childs(group)
    dists = [child[1] for child in pt.childs]
    shortest_dist = min(dists)
    # First child that is shortest distance away is chosen, rest are ignored.
    for child, dist in pt.childs:
        if dist == shortest_dist:
            # Remove current point from group so it is not used as a child in
            # next iteration
            group.discard(pt)
            return hamilton(group=group, pt=child, path=path)


shortest_len = 1000000
for node in nodes:
    # print("USING: ", node)
    L = hamilton(group=set(nodes), pt=node, path=[])
    final_result = L[0].value

    # Concatenates all the permutations together.
    for i, word in enumerate(L):
        current_word = word.value
        if i == len(L) - 1:
            if len(final_result) < shortest_len:
                shortest_len = len(final_result)
                shortest_res = final_result
        else:
            next_word = L[i + 1].value
            for j in range(len(next_word)):
                if current_word[j] == next_word[0]:
                    final_result += next_word[len(next_word) - j:]

print("Final result is of length {} and = {}".format(
    len(shortest_res), shortest_res))
