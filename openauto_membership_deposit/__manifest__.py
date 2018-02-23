# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

{
    'name': 'Openauto Membership Deposit',
    'version': '1.0',
    'category' : 'Project',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'summary': """This module Help to store deposit related informations.""",
    'description': """

Menus:
Deposit Amount

    """,
    'author': 'Openauto',
    'website': 'http://www.openauto.ch',
    'depends': [
                'base_company',
                'base_employee',
                'openauto_membership_subscription',
#               'base_fleet_reservation',
    ],
    'data':[
            'security/ir.model.access.csv',
            'data/membership_deposit_sequence_view.xml',
            'report/member_deopsit_report_view.xml',
            'views/hr_employee_views.xml',
            'views/membership_deposit_view.xml',
            'views/res_user_view.xml',
            'views/res_partner_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
