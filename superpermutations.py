"""Created by Byebrid. The hamilton() function will take in a list of permutations of an alphabet (see code near bottom) and
return a superpermutation with a length as defined by the lower bound (see bounds()), if it exists. Because of the massive
nature of this problem, this function is really too slow to do any alphabet over 3 letters long and could certainly be refined and improved.
"""
from itertools import permutations, combinations
from math import factorial


def bounds(alphabet):
    """Finds lower & upper bounds of superperumtation length of given alphabet.
    See OEIS to see where these formulae came from.
    """

    n = len(alphabet)

    lower_bound = factorial(n) + factorial(n - 1) + factorial(n - 2) + n - 3

    if n >= 7:
        upper_bound = (factorial(n) + factorial(n - 1) + factorial(n - 2)
                       + factorial(n - 3) + n - 3)
    else:
        upper_bound = 0
        for k in range(1, n + 1):
            p = len(list(permutations(alphabet, k)))
            c = len(list(combinations(alphabet, k)))
            upper_bound += p / c

    return (lower_bound, upper_bound)


def dist_btwn(self, other):
    """Finds 'distance' between 2 nodes."""
    for d, char in enumerate(self):
        self_end = self[d:]
        if other.startswith(self_end):
            dist = len(other) - len(self_end)
            return dist

    # If end of self does not begin other, then dist would just be len(other)
    return len(other)


def concatenate(path):
    """Given path, will concatenate all terms in path.

    Example: >>> concatenate(['ACB', 'CBA', 'BCA'])
             ACBABCA

    """
    print("Concatenating ", path)

    # Result starts off with first word
    result = path[0]

    for i, word in enumerate(path):
        if word == path[-1]:
            return result

        next_word = path[i + 1]

        for j in range(len(word)):
            word_end = word[j:]
            if next_word.startswith(word_end):
                # Number of characters we need to remove from start of next_word
                # because they're already at end of word.
                dist = len(word_end)
                result += next_word[dist:]
                break
            elif j == len(word) - 1:
                result += next_word


def not_in_path(perms, path):
    """Will return list of all elements of graph that are not already in path"""
    L = []
    for node in perms:
        if not node in path:
            L.append(node)
    return L


def hamilton(perms, pt=None, path=None, length=None):
    """Designed with superpermutations in mind. Will recursively go through all
    possible combinations of permutations of the alphabet (i.e. ABC, ACB, etc.).
    If length becomes too great (assuming a superperm with length = lower_bound)
    will always be possible), then goes no fruther down that path.
    """

    '''If this is the original call of hamilton(), loop through all the initial
    nodes.'''
    if pt is None:
        # Goes through first layer of tree.
        for s in perms:
            print("Using {} as root node".format(s))
            H = hamilton(perms, pt=s, path=[s], length=len(s))
            # If H does not return a successful path, then just keep going
            if H is None:
                continue
            answer = concatenate(H)
            return "Length: {}. Result is {}".format(len(answer), answer)
        # If we didn't get any result from any path, panic!
        return "NOTHING FOUND!"

    unvisited = not_in_path(perms, path)

    '''Identify if superpermutation has become too long.  Else, see if we have
    successfully found superpermutation of length lower_bound.'''
    if length > lower_bound:
        return None
    if len(unvisited) == 0:
        return path

    for child in unvisited:
        new_path = path + [child]
        new_length = length + dist_btwn(pt, child)

        H = hamilton(perms=perms, pt=child,
                     path=new_path, length=new_length)

        if H is None:
            continue
        else:
            return H


alphabet = "ABC"
lower_bound, upper_bound = bounds(alphabet)
print("Length must be between {} and {}".format(lower_bound, upper_bound))

# Finding all permutations of alphabet.
perms = [''.join(p) for p in permutations(alphabet)]

print(hamilton(perms=perms))
