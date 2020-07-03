# -*- coding: utf-8 -*-

##############################################################################
#
# ECSL Export for HMRC
# Copyright (C) 2015 OpusVL (<http://opusvl.com/>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re


def strip_leading_letters(instr):
    """Strip the leading letters off a string.

    >>> strip_leading_letters('GB12345678')
    '12345678'
    """
    return re.sub(r'^[A-Z]+', r'', instr, count=1)


def strip_country_code(instr):
    return instr[2:]


def remove_all_dashes_and_spaces(instr):
    """Remove dashes and spaces from a string.

    >>> remove_all_dashes_and_spaces('  12 34-56 78  ')
    '12345678'
    """
    return re.sub(r'[\s-]', r'', instr)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
