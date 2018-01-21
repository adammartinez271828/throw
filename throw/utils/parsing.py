#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from collections import namedtuple
import re


Token = namedtuple('Token', ['type', 'value'])
OpToken = namedtuple(
    'OpToken', ['type', 'value', 'precedence', 'associativity'])
OpInfo = namedtuple('OpInfo', ['precedence', 'associativity'])

# Assign precedence and associativity to each operator for OpTokens
OPINFO_MAP = {
    '+': OpInfo(10, 'LEFT'),
    '-': OpInfo(10, 'LEFT'),
    '*': OpInfo(20, 'LEFT'),
    '/': OpInfo(20, 'LEFT'),
    '^': OpInfo(30, 'RIGHT'),
}


class Tokenizer:
    """Provide an iterable of tokens generated from a string
    """
    # Define tokens
    token_specification = (
        ('DIE', r'\d+d-?\d+'),   # Die
        ('MODIFIER', r'\d+'),       # Modifier
        ('BINOP', r'[+\-*/^]'),  # Arithmetic operators
        ('LPAREN', r'[\(]'),      # Parentheses
        ('RPAREN', r'[\)]'),      # Parentheses
        ('SKIP', r'[ \t]+'),    # Skip over spaces and tabs
        ('MISMATCH', r'.'),         # Any other character
    )

    # Build the regex string -- essentially concatenate a bunch of regex
    # match groups.
    token_regex = '|'.join('(?P<%s>%s)' %
                           pair for pair in token_specification)

    def __init__(self, source, add_parens=True, add_opinfo=True):
        if add_parens:
            self.source = '(' + source + ')'
        else:
            self.source = source
        self.add_opinfo = add_opinfo

    def __iter__(self):
        for match in re.finditer(self.token_regex, self.source):
            ttype = match.lastgroup
            value = match.group(ttype)

            if ttype == 'SKIP':
                pass
            elif ttype == 'MISMATCH':
                raise ValueError(f'Unrecognized symbol: {value}')
            else:
                if self.add_opinfo and ttype == 'BINOP':
                    yield OpToken(ttype, value, *OPINFO_MAP[value])
                else:
                    yield Token(ttype, value)

    def __repr__(self):
        return f'Tokenizer(source={self.source})'


class FixConverter:
    """Convert lists of tokens from one *fix to another *fix
    """

    def convert_in_postfix(self, token_list):
        """Convert a list of tokens in infix order to postfix order

        Args:
            token_list: list of Tokens or OpTokens in infix order

        Returns:
            (list) the token_list in postfix order
        """
        stack = []
        out = []

        for token in list(token_list):
            if token.type == 'LPAREN':
                stack.append(token)
            elif token.type == 'BINOP':
                precedence = OPINFO_MAP[token.value].precedence
                while (self.peek_token(stack).type == 'BINOP' and
                       OPINFO_MAP[self.peek_token(stack).value].precedence >= precedence):
                    out.append(stack.pop())
                stack.append(token)
            elif token.type == 'RPAREN':
                while self.peek_token(stack).type != 'LPAREN':
                    out.append(stack.pop())
                stack.pop()  # discard the remaining paren
            else:
                out.append(token)  # operand

        return out

    def convert_in_prefix(self, token_list):
        """Convert a list of tokens in infix order to prefix order

        Args:
            token_list: list of Tokens or OpTokens in infix order

        Returns:
            (list) the token_list in prefix order
        """
        stack = []
        out = []

        for token in reversed(list(token_list)):
            if token.type == 'RPAREN':
                stack.append(token)
            elif token.type == 'BINOP':
                precedence = OPINFO_MAP[token.value].precedence
                while (self.peek_token(stack).type == 'BINOP' and
                       OPINFO_MAP[self.peek_token(stack).value].precedence >= precedence):
                    out.append(stack.pop())
                stack.append(token)
            elif token.type == 'LPAREN':
                while self.peek_token(stack).type != 'RPAREN':
                    out.append(stack.pop())
                stack.pop()  # discard the remaining paren
            else:
                out.append(token)  # operand

        return list(reversed(out))

    @staticmethod
    def peek_token(token_list):
        try:
            return token_list[-1]
        except IndexError:
            raise RuntimeError('FixConverter: Unable to peek next token!')
