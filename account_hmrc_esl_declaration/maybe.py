#!/usr/bin/env python

"""Construct pipelines of functions, in the context that any
function in the pipeline can return None, in which case the
whole computation must return None.

It should work on Python 2.7 or Python 3.
"""

def maybe(value, *functions):
    """Return result of applying successive functions to a value.

    If any of the intermediate values is None, then None is returned
    immediately, short-circuiting the rest of the calls.

    Basically, this does on your behalf the check for whether each
    successive function returned None, leaving you with a vertical column of
    functions instead of a staircase of repetitive if statements or oddly-nested
    "x if B else y" expressions.

    So this:
        result = None if x is None else x.rstrip()

    becomes this:

    >>> from .mappings import lookup
    >>> from operator import methodcaller as send
    >>> maybe(None, send('rstrip'))
    >>> maybe('abcde    ', send('rstrip'))
    'abcde'

    If you have a series of operations to perform, each on the result of the
    previous operation, you can just put each operation in like so:

    >>> maybe({'a': 'xyz  '}, lookup('a'), send('rstrip'))
    'xyz'
    >>> maybe({}, lookup('a'), send('rstrip'))
    >>> maybe(None, lookup('a'), send('rstrip'))

    """
    return _gen_maybe((None,), value, functions)

def odoo_maybe(value, *functions):
    """Like maybe, but treats False as a null value too, so suitable
    for dealing with values from Odoo models.

    Bear in mind that False can also be a valid value for a boolean
    field, so use with care.

    >>> from .mappings import lookup
    >>> from operator import methodcaller as send
    >>> odoo_maybe(None, send('rstrip'))
    >>> odoo_maybe(False, send('rstrip'))
    False
    >>> odoo_maybe('abcde    ', send('rstrip'))
    'abcde'
    >>> odoo_maybe({'a': 'xyz  '}, lookup('a'), send('rstrip'))
    'xyz'
    >>> odoo_maybe({'a': False}, lookup('a'), send('rstrip'))
    False
    >>> odoo_maybe(None, lookup('a'), send('rstrip'))
    >>> odoo_maybe(False, lookup('a'), send('rstrip'))
    False
    """
    return _gen_maybe((None, False), value, functions)

def _gen_maybe(nulls, value, functions):
    for fun in functions:
        if value in nulls:
            return value
        else:
            value = fun(value)
    return value

def maybe_c(*functions):
    """maybe_c(*functions)(value) -> maybe(value, *functions)

    Curried, so suitable for use as arguments to higher-order functions.

    >>> from operator import methodcaller as send
    >>> from .mappings import lookup
    >>> list(map(
    ...     maybe_c(lookup('a'), send('rstrip')),
    ...     [{'a': 'abc  '}, {}, None]
    ... ))
    ['abc', None, None]
    """
    return lambda value: maybe(value, *functions)

def odoo_maybe_c(*functions):
    """odoo_maybe_c(*functions)(value) -> odoo_maybe(value, *functions)

    Curried, so suitable for use as arguments to higher-order functions.
    """
    return lambda value: odoo_maybe(value, *functions)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

__copyright__ = """
Copyright (c) 2015 Nicholas Booker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
