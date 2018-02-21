# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

{
    'name': 'Openauto - Base Fleet',
    'price': 0.0,
    'currency': 'EUR',
    'version': '1.0',
    'category': 'Project',
    'license': 'Other proprietary',
    'summary': """This module send auto Response/mail.""",
    'description': """
Send mail to the customer or
/and message Followers or/and Internal Users
Send mail by selection from the stage configuration
send mail by stage configuration setting
    """,
    'author': "Openauto",
    'website': "http://www.openauto.ch",
    'images': ['static/description/img1.jpg'],
    'depends': ['fleet',
                'base_company',
                'base_employee'],
    'data': [
            'views/vehicle_type_view.xml',
            'views/vehicle_sub_type_view.xml',
            'views/fleet_vehicle_view.xml',
            'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
