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

from operator import methodcaller

class AccountVatESLWizard(models.TransientModel):
    # Based on odoo/addons/account/wizard/account_vat.py from upstream Odoo.
    # Code used and modified under AGPL v3.

    _name = 'account.vat.esl'
    _description = 'EC Sales Declaration'
    _inherit = 'account.common.report'

    period_from = fields.Many2one(string='Period', required=True)   # We only care about one period

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
        default=methodcaller('_default_chart_of_taxes'),
    )

    def _default_chart_of_taxes(self):
        taxes = self.env['account.tax.code'].search(
            [
                ('company_id', '=', self.env.user.company_id.id),
                ('name', '=ilike', '%Total value of EC sales, ex VAT%'),
            ],
            limit=1,
        )
        return taxes and taxes.id or False

    @api.multi
    def create_esl(self):
        """This should be triggered by the form.
        """
        self.ensure_one()

        # TODO Return the action that will trigger the query and its CSV download
        return False

        # Here's the create_vat() code from upstream - some of it may be relevant here
        # if context is None:
        #     context = {}

        # datas = {'ids': context.get('active_ids', [])}
        # datas['model'] = 'account.tax.code'
        # datas['form'] = self.read(cr, uid, ids, context=context)[0]

        # for field in datas['form'].keys():
        #     if isinstance(datas['form'][field], tuple):
        #         datas['form'][field] = datas['form'][field][0]

        # taxcode_obj = self.pool.get('account.tax.code')
        # taxcode_id = datas['form']['chart_tax_id']
        # taxcode = taxcode_obj.browse(cr, uid, [taxcode_id], context=context)[0]
        # datas['form']['company_id'] = taxcode.company_id.id

        # return self.pool['report'].get_action(cr, uid, [], 'account.report_vat', data=datas, context=context)

    def declaration_year(self):
        """Return year of declaration in YYYY format."""
        # NOTE This assumes period name is in MM/YYYY format
        return self.period_from.name.split('/')[1]

    def declaration_month(self):
        """Return month of declaration in MM format."""
        # NOTE This assumes period name is in MM/YYYY format
        return self.period_from.name.split('/')[0]

    @api.multi
    def esl_csv_records(self):
        """Return the CSV records in HMRC-compatible format as a list of rows.
        """
        self.ensure_one()

        company = self.chart_tax_id.company_id
        title_record = ['HMRC_CAT_ESL_BULK_SUBMISSION_FILE']
        header_record = [
            company.vat,
            company.subsidiary_identifier,
            self.declaration_year(),
            self.declaration_month(),
            'GBP',
            company.name[:35], # NOTE truncating might not be sufficient
        ]
        line_records = [
            # TODO
        ]
        return [ title_record, header_record ] + line_records

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
