# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.
{
    'name': 'openauto_expense',
    'version': '1.0',
    'category' : 'Sales',
    'license': 'Other proprietary',
    'currency': 'EUR',
    'summary': """This module allow Handle vehicle expenses.""",
    'description': """

This module allow Handle vehicle expenses
    """,
    'author': 'Openauto',
    'website': 'http://www.openauto.ch',
    'depends': [
                'hr_expense',
#                'base_fleet',
                'base_fleet_reservation',
    ],
    'data':[
            'data/vehicle_service_data.xml',
            'report/expense_report_view.xml',
            'views/vehicle_expense_form_view.xml',
            'views/vehicle_expense_sheet_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
