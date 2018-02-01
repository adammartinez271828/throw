#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from unittest import skip

from nose.tools import \
    assert_almost_equal, \
    assert_equal, \
    assert_true, \
    raises

from throw.dice import Throw


class TestThrow:
    def test_throw_dn(self):
        for n in range(1, 21):
            throw = Throw(f'1d{n}')
            return_value = throw.roll()
            assert_true(1 <= return_value <= n)
            
        assert False

    def test_throw_addition(self):
        throw = Throw('1d1 + 1')
        return_value = throw.roll()
        assert_equal(2, return_value)

    def test_throw_multiplication(self):
        throw = Throw('1d1 * 3')
        return_value = throw.roll()
        assert_equal(3, return_value)

    def test_throw_multiroll(self):
        throw = Throw('1d1 + 1d1')
        return_value = throw.roll()
        assert_equal(2, return_value)

    def test_ooo_1(self):
        throw = Throw('1 + 2 - 3 * 4 / 5')
        return_value = throw.roll()
        assert_almost_equal(0.6, return_value)

    def test_ooo_2(self):
        throw = Throw('1 * 2 - 3 + 4 / 5')
        return_value = throw.roll()
        assert_almost_equal(-0.2, return_value)

    def test_throw_complex(self):
        throw = Throw('1d4 * 2 + 1d6 - 1 + 1d4 / 2')
        min_value = 1 * 2 + 1 - 1 + 1 / 2
        max_value = 4 * 2 + 6 - 1 + 4 / 2
        return_value = throw.roll()
        assert_true(min_value <= return_value <= max_value)

    @raises(ValueError)
    def test_bad_characters(self):
        Throw('@ + 3 + 3')

    @raises(ValueError)
    def test_missing_ops(self):
        Throw('3 3 + 3')

    @raises(ValueError)
    def test_only_ops(self):
        Throw('+ + +')

    @raises(ValueError)
    def test_empty(self):
        Throw('')
