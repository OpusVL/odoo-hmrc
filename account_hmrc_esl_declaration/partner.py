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

class ResPartnerHMRC(models.Model):
    _inherit = 'res.partner'

    HMRC_SUPPLIER_INDICATOR_OPTIONS = [
        ('b2b_goods', 'B2B Goods'),
        ('tri_intermediary', 'Intermediary in a triangular transaction'),
        ('b2b_services', 'B2B Services'),
    ]

    ESL_INDICATOR_MAP = {
        False: False,
        'b2b_goods': '0',
        'tri_intermediary': '2',
        'b2b_services': '3',
    }

    hmrc_supplier_indicator = fields.Selection(
        selection=HMRC_SUPPLIER_INDICATOR_OPTIONS,
        string='HMRC Supplier Indicator',
    )

    esl_indicator_code = fields.Char(compute='_esl_indicator_code_compute',)

    @api.depends('hmrc_supplier_indicator')
    @api.one
    def _esl_indicator_code_compute(self):
        self.esl_indicator_code = self.ESL_INDICATOR_MAP[self.hmrc_supplier_indicator]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
