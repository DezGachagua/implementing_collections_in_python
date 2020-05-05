from bisect import bisect_left
from collections.abc import Sequence, Set
from itertools import chain


class SortedSet(Sequence, Set):
    # the sorted set will be created from sequences...
    # ...  and iterables and have it ignore duplicates
    def __init__(self, items=None):
        # we create a list using sorted built in function
        # set constructor is a good model for the SortedSet constructor
        self._items = sorted(set(items)) if items is not None else []

    # container protocol method
    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    # len(sized) protocol method
    def __len__(self):
        return len(self._items)

    # iterator protocol method
    def __iter__(self):
        return iter(self._items)

    # sequence protocol
    # __getitem__ () method for the list indexing operator
    # def __getitem__(self, index):
    #     return self._items[index]

    # step args for slice attr is not used so it defaults to none
    def __getitem__(self, index):
        return self._items[index]
        return SortedSet(result) if isinstance(index, slice) else result

    def __repr__(self):
        return "SortedSet({})".format(
            repr(self._items) if self._items else ''
        )

    """implementing equality and inequality with __eq__() and __ne__() methods respectively
        Args:
            rhs: right hand side operand
            lhs: left hand side operand(self arg) 
        Returns:
            NotImplemented: built in singleton that returns if the types don't match"""
    def __eq__(self, rhs):
        # type check
        if not isinstance(rhs, SortedSet):
            return NotImplemented
        return self._items == rhs._items

    def __ne__(self, rhs):
        # type check
        if not isinstance(rhs, SortedSet):
            return NotImplemented
        return self._items != rhs._items

    # asserting assumptions as true
    def _is_unique_and_sorted(self):
        return all(self[i] < self[i + 1] for i in range(len(self) - 1))

    """ index() method
        Uses: 
            bisect_left function from bisect module to search for an item returning
                the index at which requested item should placed in the sequence
        Tests:
            1st: checks whether returned index is within bounds of collection
            2nd: checks whether there is already the required item at that index
        Returns: 
            0 and 1 for true and false respectively after conversion of bool to int"""
    def index(self, item):
        assert self._is_unique_and_sorted()
        index = bisect_left(self._items, item)
        if (index != len(self._items)) and (self._items[index] == item):
            return index
        raise ValueError("{} not found".format(repr(item)))

    # simply converts result from membership test to an integer
    # membership test in container protocol method
    def count(self, item):
        assert self._is_unique_and_sorted()
        return int(item in self)

    # concatenation
    def __add__(self, rhs):
        return SortedSet(chain(self._items, rhs._items))

    # repetition/multiplication
    def __mul__(self, rhs):
        return self if rhs > 0 else SortedSet()

    # reversed multiplication
    def __rmul__(self, lhs):
        return self * lhs

    def issubset(self, iterable):
        return self <= SortedSet(iterable)

    def issuperset(self, iterable):
        return self >= SortedSet(iterable)

    def intersection(self, iterable):
        return self & SortedSet(iterable)

    def union(self, iterable):
        return self | SortedSet(iterable)

    def symmetric_difference(self, iterable):
        return self ^ SortedSet(iterable)

    def difference(self, iterable):
        return self - SortedSet(iterable)