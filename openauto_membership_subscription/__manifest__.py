# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

{
    'name': 'openauto_membership_subscription',
    'version': '1.0',
    'category' : 'Project',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'summary': """This module help to made membreship.""",
    'description': """

Menus:
Sales

    """,
    'author': 'Openauto',
    'website': 'http://www.openauto.ch',
    'depends': [
                'base_fleet_reservation',
                'contract_recurring_invoice_analytic',
    ],
    'data': [
            'views/membership_renew_view.xml',
            'views/analytic_view.xml',
            'views/sale_view.xml',
            'reports/contract_recurring_invoice_analytic_report.xml'
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
