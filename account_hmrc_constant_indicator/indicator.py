# -*- coding: utf-8 -*-

##############################################################################
#
# Constant indicator for HMRC account
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
from openerp.addons.account_hmrc_esl_declaration.indicator import INDICATOR_SELECTION

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('account_id.company_id.constant_transaction_indicator_type')
    @api.one
    def _transaction_indicator_type_compute(self):
        company = self.account_id.company_id
        self.transaction_indicator_type = company.constant_transaction_indicator_type



class ResCompany(models.Model):
    _inherit = 'res.company'

    constant_transaction_indicator_type = fields.Selection(INDICATOR_SELECTION,
        required=True,
        default='b2b_goods',
        help='All line items on ESL export for this company will be assumed to have the selected type.',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
