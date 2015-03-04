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

INDICATOR_SELECTION = [
    ('b2b_goods', 'B2B Goods'),
    ('triangular', 'Supplier is an intermediary in a triangular transaction'),
    ('b2b_services', 'B2B Services'),
]

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    transaction_indicator_type = fields.Selection(INDICATOR_SELECTION,
        compute='_transaction_indicator_type_compute',
        store=True,
    )

    @api.one
    def _transaction_indicator_type_compute(self):
        """OVERRIDE. Set the transaction_indicator_type.

        You should set it to 'b2b_goods', 'triangular' or 'b2b_services' in an
        _inherit of your own.

        Here's an (as yet untested) example:

        # TODO test this
        @api.depends('company_id.transaction_type')
        @api.one
        def _transaction_type_compute(self):
            self.transaction_indicator_type = self.company_id.transaction_type
        """
        raise NotImplementedError(
            'Override _transaction_type_compute to set transaction_indicator_type field'
        )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
