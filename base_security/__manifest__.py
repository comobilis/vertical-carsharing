# -*- coding: utf-8 -*-

# Part of Openauto.
#See LICENSE file for full copyright and licensing details.

{
    'name': 'Openauto - Base Security',
    'price': 0.0,
    'currency': 'EUR',
    'version': '1.0',
    'category': 'Project',
    'license': 'Other proprietary',
    'summary': """Openauto - Base Employee""",
    'description': """
    """,
    'author': "Openauto",
    'website': "http://www.openauto.ch",
    'depends': [
        'openauto_expense',
        'openauto_membership_deposit',
        'vehicle_reservation_notification'
    ],
    'data': [
        'security/reservation_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
