#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from nose.tools import \
    assert_list_equal, \
    assert_equal, \
    assert_true, \
    raises

from throw.utils.parsing import \
    FixConverter, \
    OpInfo, \
    OpToken, \
    Token, \
    Tokenizer


class TestTokenizer:

    def test_iterable(self):
        test_string = '1 + 1'
        for _ in Tokenizer(test_string):
            pass

    def test_generates_tokens(self):
        test_string = '1 + 1'
        assert_true(all(isinstance(item, Token) or isinstance(item, OpToken)
                        for item in Tokenizer(test_string)))

    def test_print(self):
        test_string = '1 + 1'
        target_string = 'Tokenizer(source=(1 + 1))'
        assert_equal(str(Tokenizer(test_string)), target_string)

    def test_catchall(self):
        test_string = '1 + (2 - 3) * 4 / 5 ^ 6'
        target_list = [
            Token(type='LPAREN', value='('),
            Token(type='MODIFIER', value='1'),
            OpToken(type='BINOP', value='+',
                    precedence=10, associativity='LEFT'),
            Token(type='LPAREN', value='('),
            Token(type='MODIFIER', value='2'),
            OpToken(type='BINOP', value='-',
                    precedence=10, associativity='LEFT'),
            Token(type='MODIFIER', value='3'),
            Token(type='RPAREN', value=')'),
            OpToken(type='BINOP', value='*',
                    precedence=20, associativity='LEFT'),
            Token(type='MODIFIER', value='4'),
            OpToken(type='BINOP', value='/',
                    precedence=20, associativity='LEFT'),
            Token(type='MODIFIER', value='5'),
            OpToken(type='BINOP', value='^',
                    precedence=30, associativity='RIGHT'),
            Token(type='MODIFIER', value='6'),
            Token(type='RPAREN', value=')')
        ]

        assert_list_equal(list(iter(Tokenizer(test_string))), target_list)


class TestFixConverter:

    def test_infix_to_prefix(self):
        infix_token_list = Tokenizer('1 / (4 + 5) + 1d6 ^ 3')
        target_token_list = [
            OpToken(type='BINOP', value='+',
                    precedence=10, associativity='LEFT'),
            OpToken(type='BINOP', value='/',
                    precedence=20, associativity='LEFT'),
            Token(type='MODIFIER', value='1'),
            OpToken(type='BINOP', value='+',
                    precedence=10, associativity='LEFT'),
            Token(type='MODIFIER', value='4'),
            Token(type='MODIFIER', value='5'),
            OpToken(type='BINOP', value='^',
                    precedence=30, associativity='RIGHT'),
            Token(type='DIE', value='1d6'),
            Token(type='MODIFIER', value='3')
        ]

        assert_list_equal(FixConverter().convert_in_prefix(
            infix_token_list), target_token_list)

    def test_infix_to_postfix(self):
        infix_token_list = Tokenizer('1 / (4 + 5) + 1d6 ^ 3')
        target_token_list = [
            Token(type='MODIFIER', value='1'),
            Token(type='MODIFIER', value='4'),
            Token(type='MODIFIER', value='5'),
            OpToken(type='BINOP', value='+',
                    precedence=10, associativity='LEFT'),
            OpToken(type='BINOP', value='/',
                    precedence=20, associativity='LEFT'),
            Token(type='DIE', value='1d6'),
            Token(type='MODIFIER', value='3'),
            OpToken(type='BINOP', value='^',
                    precedence=30, associativity='RIGHT'),
            OpToken(type='BINOP', value='+',
                    precedence=10, associativity='LEFT')
        ]

        assert_list_equal(FixConverter().convert_in_postfix(
            infix_token_list), target_token_list)
