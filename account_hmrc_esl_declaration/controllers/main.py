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

import simplejson

from openerp.tools import html_escape
from openerp.addons.web.http import Controller, route, request
from openerp.addons.web.controllers.main import (
    content_disposition,
    _serialize_exception,
)

class HMRCController(Controller):
    @route('/hmrc/esl/<id>', type='http', auth='user')
    def esl_download(self, id):
        try:
            ESLWizard = request.registry['account.vat.esl']
            esl = ESLWizard.browse(request.cr, request.uid, int(id))
            if esl:
                filecontent = esl.esl_csv_data()
                period_name = esl.period_from.name
                filename = 'esl_%s.csv' % (period_name,)
                return request.make_response(
                    filecontent,
                    headers=[
                        ('Content-Type', 'text/csv'),
                        ('Content-Disposition', content_disposition(filename)),
                    ],
                )
            else:
                return request.not_found()
        except Exception, e:
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': _serialize_exception(e),
            }
            return request.make_response(html_escape(simplejson.dumps(error)))



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
