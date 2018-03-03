# -*- coding: utf-8 -*-

# Part of Openauto.
#See LICENSE file for full copyright and licensing details.
{
    'name': 'Openauto Report',
    'version': '1.0',
    'category' : 'Project',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'summary': """This module allow Print Report of the documents.""",
    'description': """

Menus:
Sales

    """,
    'author': 'Openauto',
    'website': 'http://www.openauto.ch',
#    'images': ['static/description/img1.jpg'],
#    'live_test_url': 'https://youtu.be/gkU-pnHNUGc',
    'depends': [
        'base_fleet_reservation',
    ],
    'data':[
            'wizard/booking_report_wiz_view.xml',
            'report/booking_report_view.xml',
            'report/reservation_schedule_report_view.xml',
            'report/event_report.xml',
            'views/menu.xml',
            'views/calendar_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
