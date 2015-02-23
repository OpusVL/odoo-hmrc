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

from openerp import models, fields, api

class ResCompanyHMRC(models.Model):
    _inherit = 'res.company'

    subsidiary_identifier = fields.Char(
        size=3,
        required=True,
        default='000',
        help='for HMRC documents such as the ESL declaration.  If you have, none, set to 000',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
