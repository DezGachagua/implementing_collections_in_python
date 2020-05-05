""" A way of how to implement collections in Python through some tests

    Collection protocols include:
        Container: allows for testing of item membership(using in and not in) in a collection.
        Sized: determine number of elements in a collection.
        Iterable: allows iteration over elements in a collection.
        Sequence: supports random read access in collections.
        Set: allows operations on elements through it's set operators

    Reference: collections.abc documentation at python.org"""


# the unittest module provides a test framework for our test suites

import unittest
# simple way to determine whether a class implements a particular protocol
from collections import Set
from collections.abc import (Container, Sized, Iterable, Sequence)
from sorted_set import SortedSet

""" the tests will check that we are able to construct instances
of SortedSet as like from any Python collection"""


class TestConstruction(unittest.TestCase):

    # testing  with an empty list
    def test_empty(self):
        s = SortedSet([])

    # testing with a list containing some items
    def test_from_sequence(self):
        s = SortedSet([7, 8, 3, 14, 21, 35])

    # testing with a list containing duplicate items
    def test_with_duplicates(self):
        s = SortedSet([8, 8, 8])

    # testing with an arbitrary iterable(a generator that is)
    def test_from_iterable(self):
        def gen6842():
            yield 6
            yield 8
            yield 4
            yield 2
        g = gen6842()
        s = SortedSet(g)

    # test to construct a SortedSet with no args with no exception being raised
    def test_default_empty(self):
        s = SortedSet()


""" Container Protocol. """


class TestContainerProtocol(unittest.TestCase):

    # we override this function to create a sorted set
    def setUp(self):
        self.s = SortedSet([9, 8, 7, 6])
    # test cases to check for positive and negative results for in and not in operators
    def test_positive_contained(self):
        self.assertTrue(9 in self.s)

    def test_negative_contained(self):
        self.assertFalse(2 in self.s)

    def test_positive_not_contained(self):
        self.assertTrue(4 not in self.s)

    def test_negative_not_contained(self):
        self.assertFalse(6 not in self.s)

    # test to check for inheritance from Container
    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Container))


""" Sized Protocol. """


class TestSizedProtocol(unittest.TestCase):

    def test_empty(self):
        s = SortedSet()
        self.assertEqual(len(s), 0)

    def test_one(self):
        s = SortedSet([42])
        self.assertEqual(len(s), 1)

    def test_ten(self):
        s = SortedSet(range(10))
        self.assertEqual(len(s), 10)

    #  test ensures duplicate items passed to constructor are only counted once
    def test_with_duplicates(self):
        s = SortedSet([5, 5, 5])
        self.assertEqual(len(s), 1)

    # test to check for inheritance from Sized
    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Sized))


""" Iterable Protocol. """


class TestIterableProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedSet([7, 2, 3, 1, 1, 9])

    def test_iter(self):
        i = iter(self.s)
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)
        self.assertEqual(next(i), 3)
        self.assertEqual(next(i), 7)
        self.assertEqual(next(i), 9)
        # call to assertRaises passes a nullary lambda with no args so as assertion...
        #... can call next(i) rather than the code doing that and passing result to next assertion
        self.assertRaises(StopIteration, lambda: next(i))

    def test_for_loops(self):
        index = 0
        expected = [1, 2, 3, 7, 9]
        for item in self.s:
            self.assertEqual(item, expected[index])
            index += 1

    # test to check for inheritance from Iterable
    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Iterable))


""" Sequence Protocol. """


class TestSequenceProtocol(unittest.TestCase):

    """ Indexing.
    __getitem__() method provides forward and reversed indexing with
    negative integers. """

    # forward indexing
    def setUp(self):
        self.s = [1, 4, 9, 13, 15]

    def test_index_zero(self):
        self.assertEqual(self.s[0], 1)

    def test_index_four(self):
        self.assertEqual(self.s[4], 15)

    def test_index_beyond_the_end(self):
        with self.assertRaises(IndexError):
            self.s[5]

    #  reversed indexing
    def test_index_minus_one(self):
        self.assertEqual(self.s[-1], 15)

    def test_index_minus_five(self):
        self.assertEqual(self.s[-5], 1)

    def test_index_one_before_the_beginning(self):
        with self.assertRaises(IndexError):
            self.s[-6]

    """ Slicing """
    def test_slice_from_start(self):
        self.assertEqual(self.s[:3], [1, 4, 9])

    def test_slice_from_end(self):
        self.assertEqual(self.s[3:], [13, 15])

    def test_slice_empty(self):
        self.assertEqual(self.s[10:], [])

    # test for an arbitrary slice with start index: 2 and stop index: 4
    def test_slice_arbitrary(self):
        self.assertEqual(self.s[2:4], [9, 13])

    # test full slice
    def test_slice_full(self):
        self.assertEqual(self.s[:], self.s)

    """ Reversing """
    def test_reversed(self):
        s = SortedSet([1, 3, 5, 7])
        r = reversed(s)
        self.assertEqual(next(r), 7)
        self.assertEqual(next(r), 5)
        self.assertEqual(next(r), 3)
        self.assertEqual(next(r), 1)
        with self.assertRaises(StopIteration):
            next(r)

    """ index() 
        Returns: 
            First matching item in the collection
        Raises:
            ValueError: if item is not returned """
    def test_index_positive(self):
        s = SortedSet([1, 5, 8, 9])
        self.assertEqual(s.index(8), 2)

    def test_index_negative(self):
        s = SortedSet([1, 5, 8, 9])
        with self.assertRaises(ValueError):
            s.index(15)

    """ count()
        Returns:
            Number of times a specified item occurs in a list"""
    def test_count_zero(self):
        s = SortedSet([1, 5, 7, 9])
        self.assertEqual(s.count(11), 0)

    def test_count_one(self):
        s = SortedSet([1, 5, 7, 9])
        self.assertEqual(s.count(7), 1)

    # test to check for inheritance from Sequence
    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Sequence))

    """ Concatenation. """
    def test_concatenate_disjoint(self):
        s = SortedSet([1, 2, 3])
        t = SortedSet([4, 5, 6])
        self.assertEqual(s + t, SortedSet([1, 2, 3, 4, 5, 6]))

    def test_concatenate_equal(self):
        s = SortedSet([2, 4, 6])
        self.assertEqual(s + s, s)

    def test_concatenate_intersecting(self):
        s = SortedSet([1, 2, 3])
        t = SortedSet([3, 4, 5])
        self.assertEqual(s + t, SortedSet([1, 2, 3, 4, 5]))

    """ Repetition/ Multiplication """
    def test_repetition_zero_right(self):
        s = SortedSet([4, 5, 6])
        self.assertEquals(s * 0, SortedSet())

    def test_repetition_nonzero_right(self):
        s = SortedSet([4, 5, 6])
        self.assertEquals(s * 100, s)

    # reversed repetition
    def test_repetition_zero_left(self):
        s = SortedSet([4, 5, 6])
        self.assertEquals(s * 0, SortedSet())

    def test_repetition_nonzero_left(self):
        s = SortedSet([4, 5, 6])
        self.assertEquals(s * 100, s)


""" Repr Protocol. """


class TestReprProtocol(unittest.TestCase):
    # Through these  tests, repr is expected to be a string which looks like a valid constructor call
    # Test for empty SortedSet
    def test_repr_empty(self):
        s = SortedSet()
        self.assertEqual(repr(s), "SortedSet()")

    # Test for non-empty SortedSet
    def test_repr_some(self):
        s = SortedSet([42, 40, 19])
        self.assertEqual(repr(s), "SortedSet([19, 40, 42])")


""" Equality Protocol. """


class TestEqualityProtocol(unittest.TestCase):
    def test_positive_equality(self):
        self.assertTrue(SortedSet([4, 5, 6]) == SortedSet([6, 5, 4]))

    def test_negative_equality(self):
        self.assertFalse(SortedSet([4, 5, 6]) == SortedSet([1, 2, 3]))

    # test for mismatched types: SortedSet and a regular list
    def test_type_mismatch(self):
        self.assertFalse(SortedSet([4, 5, 6]) == [4, 5, 6])

    # test is a sanity check to ensure that a SortedSet is always equal to itself
    def test_identical(self):
        s = SortedSet([10, 11, 12])
        self.assertTrue(s == s)


""" Inequality Protocol. """


class TestInequalityProtocol(unittest.TestCase):
    def test_positive_unequal(self):
        self.assertTrue(SortedSet([4, 5, 6]) != SortedSet([1, 2, 3]))

    def test_negative_unequal(self):
        self.assertFalse(SortedSet([4, 5, 6]) != SortedSet([6, 5, 4]))

    def test_type_mismatch(self):
        self.assertTrue(SortedSet([1, 2, 3]) != [1, 2, 3])

    def test_identical(self):
        s = SortedSet([10, 11, 12])
        self.assertFalse(s != s)


""" Set Protocol with relational operators. """


class TestRelationalSetProtocol(unittest.TestCase):

    # proper subset
    def test_lt_positive(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s < t)

    # proper subset
    def test_lt_negative(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s < t)

    # subset with a proper subset
    def test_le_lt_positive(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s <= t)

    # subset and equal
    def test_le_eq_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s <= t)

    # subset
    def test_le_negative(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertFalse(s <= t)

    # proper superset
    def test_gt_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertTrue(s > t)

    # proper superset
    def test_gt_negative(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s > t)

    # superset with proper superset
    def test_ge_gt_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2})
        self.assertTrue(s > t)

    # superset and equal
    def test_ge_eq_positive(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({1, 2, 3})
        self.assertTrue(s >= t)

    # superset
    def test_ge_negative(self):
        s = SortedSet({1, 2})
        t = SortedSet({1, 2, 3})
        self.assertFalse(s >= t)


""" Set Protocol with Relational Methods. """


class TestSetRelationalMethods(unittest.TestCase):

    def test_issubset_proper_positive(self):
        s = SortedSet({1, 2})
        t = [1, 2, 3]
        self.assertTrue(s.issubset(t))

    def test_issubset_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issubset(t))

    def test_issubset_negative(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2]
        self.assertFalse(s.issubset(t))

    def test_issuperset_proper_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2]
        self.assertTrue(s.issuperset(t))

    def test_issuperset_positive(self):
        s = SortedSet({1, 2, 3})
        t = [1, 2, 3]
        self.assertTrue(s.issuperset(t))

    def test_issuperset_negative(self):
        s = SortedSet({1, 2})
        t = [1, 2, 3]
        self.assertFalse(s.issuperset(t))


""" Set Protocol with Operation(Algebraic) operators. """


class TestOperationSetProtocol(unittest.TestCase):

    def test_intersection(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s & t, SortedSet({2, 3}))

    def test_union(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s | t, SortedSet({1, 2, 3, 4}))

    def test_symmetric_difference(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s ^ t, SortedSet({1, 4}))

    def test_difference(self):
        s = SortedSet({1, 2, 3})
        t = SortedSet({2, 3, 4})
        self.assertEqual(s - t, SortedSet({1}))


""" Set Protocol with Operation Methods. """


class TestSetOperationsMethods(unittest.TestCase):

    def test_intersection(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.intersection(t), SortedSet({2, 3}))

    def test_union(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.union(t), SortedSet({1, 2, 3, 4}))

    def test_symmetric_difference(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.symmetric_difference(t), SortedSet({1, 4}))

    def test_difference(self):
        s = SortedSet({1, 2, 3})
        t = [2, 3, 4]
        self.assertEqual(s.difference(t), SortedSet({1}))

    def test_isdisjoint_positive(self):
        s = SortedSet({1, 2, 3})
        t = [4, 5, 6]
        self.assertTrue(s.isdisjoint(t))

    def test_isdisjoint_negative(self):
        s = SortedSet({1, 2, 3})
        t = [3, 4, 5]
        self.assertFalse(s.isdisjoint(t))


""" test to check for inheritance from Set protocol in collections module. """


class TestSetProtocol(unittest.TestCase):

    def test_protocol(self):
        self.assertTrue(issubclass(SortedSet, Set))


# standard boilerplate for the main function
if __name__ == '__main__':
    unittest.main()
