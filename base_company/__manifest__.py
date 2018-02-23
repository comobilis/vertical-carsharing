# -*- coding: utf-8 -*-

# Part of Openauto.
#See LICENSE file for full copyright and licensing details.

{
    'name': 'Openauto - Base Company',
    'price': 0.0,
    'currency': 'EUR',
    'version': '1.0',
    'category': 'Project',
    'license': 'Other proprietary',
    'summary': """Openauto - Base Company""",
    'description': """
    """,
    'author': "Openauto",
    'website': "http://openauto.ch/",
    'depends': ['base',
                ],
    'data': [
        #'security/ir.model.access.csv',
        'views/res_company_views.xml',
#        'views/membership_payment_level.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
