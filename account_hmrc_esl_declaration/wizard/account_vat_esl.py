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

import csv
from operator import methodcaller
from itertools import starmap

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from openerp import models, fields, api
from openerp.exceptions import ValidationError

from ..maybe import odoo_maybe
from ..util import (strip_leading_letters, remove_all_dashes_and_spaces)

_INDICATOR_MAP = {
    # Mapping from transaction_indicator_type to the code used in the CSV file
    'b2b_goods': '0',
    'triangular': '2',
    'b2b_services': '3',
}

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
        return self.env['report'].get_action(self, 'account_hmrc_esl_declaration.esl_csv')


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
            odoo_maybe(company.vat,
                       remove_all_dashes_and_spaces,
                       strip_leading_letters),
            company.subsidiary_identifier,
            self.declaration_year(),
            self.declaration_month(),
            'GBP',
            company.name[:35], # NOTE truncating might not be sufficient
            '0',    # "the indicator field (this will always be '0')"
        ]
        return [ title_record, header_record ] + self._detail_records()

    @api.multi
    def _detail_records(self):
        self.ensure_one()
        self.env.cr.execute("""
            SELECT COUNTRY.code, P.vat, SUM(L.credit - L.debit), L.transaction_indicator_type
            FROM
                account_move_line AS L
                INNER JOIN res_partner AS P ON P.id = L.partner_id
                INNER JOIN account_move AS M on M.id = L.move_id
                LEFT OUTER JOIN res_country AS COUNTRY ON COUNTRY.id = P.country_id
            WHERE
                L.tax_code_id = %s
                AND L.period_id = %s
            GROUP BY COUNTRY.code, P.vat, L.transaction_indicator_type
            """,
            (self.chart_tax_id.id, self.period_from.id,),
        )
        rows = self.env.cr.fetchall()
        return list(starmap(_convert_detail_row, rows))

    @api.multi
    def esl_csv_data(self):
        """Return the CSV data as a string.
        """
        data = StringIO()
        csv.writer(data).writerows(self.esl_csv_records())
        return data.getvalue()

def _convert_detail_row(sql_country_code, sql_vat, sql_value, sql_indicator):
    """Convert an SQL row to a CSV detail row.

    >>> _convert_detail_row('FR', 'FR123456', 1000.99, 'b2b_goods')
    ['FR', '123456', '1000', '0']
    """

    # NOTE Unsure about the rounding - I've assumed to truncate the value to
    #      next lowest whole pound.
    if not sql_indicator:
        raise ValidationError([
            'Not all accounts from this period have an indicator set against the transaction_indicator_type ',
            'This may be because you have installed this module after entries have been created ',
            'The field is stored in the database, and computed on the fly. ',
            'This can be fixed with a direct sql query e.g: \n',
            "UPDATE account_move_line SET transaction_indicator_type='b2b_goods';"
        ])
    return [
        sql_country_code,
        odoo_maybe(sql_vat, remove_all_dashes_and_spaces, strip_leading_letters),
        "%d" % sql_value,
        _INDICATOR_MAP[sql_indicator],
    ]



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
