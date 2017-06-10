#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from math import isclose
import operator
from random import randint

from throw.utils.parsing import FixConverter, Tokenizer


class Throw:
    """A collection of dice, modifiers, and arithmetic

    A "Throw" represents a collection of dice, modifiers, and some arithmetic
    that binds them together.  The Throw can be "rolled", which returns some
    random result, determined by the throw's rules.

    For example:
        Throw('1d6').roll() should return a number between 1 and 6
        Throw('2d6').roll() should return a number between 2 and 12
        Throw('1d8').roll() should return a number between 1 and 8
        Throw('1d6 + 1').roll() should return a number between 2 and 7
        Throw('1d6 + 1d8 + 1').roll() should return a number between 3 and 15
    """

    def __init__(self, arith_string):
        """Initialize a Throw

        Args:
            arith_string (str): a string representing the dice and modifiers
                in the throw
        """
        self.token_list, self.roll = RollParser().parse(arith_string)


class RollParser:

    def parse(self, expression):
        """Parse a roll's arithmetic string

        An arithmetic string combines any number of simple operations with
        constants and "rolls" of dice.  A roll is of the form ndx, where n and
        x are natural numbers.

        Args:
            expression (str): a string to parse

        Returns:
            (list, function) the list of tokens and a function that can be
                invoked to generate a result from the arithmetic string
        """
        token_list = list(Tokenizer(expression))

        for token in token_list:
            if token.type == 'DIE':
                count, size = map(int, token.value.split('d'))
                if count < 1 or size < 1:
                    raise ValueError(f'Invalid die: {token.value}')

        postfix_token_list = FixConverter().convert_in_postfix(token_list)

        def roll_function(): return self.evaluate(postfix_token_list, expression)

        # Call roll_function once just to see if we can actually evaluate the expression
        roll_function()

        return token_list, roll_function

    def evaluate(self, token_list, expression):
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '^': operator.pow,
        }

        stack = []

        for token in token_list:
            if token.type != 'BINOP':
                stack.append(self._evaluate_operand(token))
            else:
                try:
                    right, left = stack.pop(), stack.pop()
                except IndexError:  # Unable to pop, means expression isn't valid
                    raise ValueError(f'Invalid expression: "{expression}"')
                stack.append(
                    ops[token.value](
                        left,
                        right,
                    )
                )

        if len(stack) != 1:
            raise ValueError(f'Invalid expression: "{expression}"')

        result = stack[0]

        if isclose(result, int(result)):
            return int(result)
        else:
            return result

    def _evaluate_operand(self, operand):
        try:
            if operand.type == 'DIE':
                dice, size = map(int, operand.value.split('d'))
                return sum(randint(1, size) for _ in range(dice))
            else:
                return float(operand.value)
        except AttributeError:  # operand isn't a token
            return float(operand)
