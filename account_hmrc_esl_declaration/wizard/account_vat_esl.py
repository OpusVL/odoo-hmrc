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

class AccountVatESLWizard(models.TransientModel):
    _name = 'account.vat.esl'
    _description = 'EC Sales Declaration'
    _inherit = 'account.common.report'

    based_on = fields.Selection(
        # Looking at how account.vat.declaration uses this, I think this field may be completely
        # redundant.  It's in the model, but hidden to the user in the UI.  So perhaps only
        # 'invoices' makes sense here.
        default='invoices',
        required=True,
        readonly=True,
        selection=[
            ('invoices', 'Invoices'),
            ('payments', 'Payments'),
        ],
        string='Based on',
    )

    chart_tax_id = fields.Many2one(
        comodel_name='account.tax.code',
        string='Chart of Tax',
        required=True,
        domain=[('parent_id', '=', False)],
    )

    @api.multi
    def create_esl(self):
        self.ensure_one()

        # TODO Return the action that will trigger the query and its CSV download
        return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
