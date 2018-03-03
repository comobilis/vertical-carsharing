# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

{
    'name': 'vehicle_reservation_notification',
    'version': '1.0',
    'category' : 'Project',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'summary': """This module help to send Notification to the partner.""",
    'description': """

Menus:

    """,
    'author': 'Openauto',
    'website': 'http://www.openauto.ch',
    'depends': [
                'base_fleet_reservation',
    ],
    'data': [
        'data/reservation_notification_template.xml',
        'data/reservation_notification_config_cron.xml',
        'data/reservation_notification_reminder_template.xml',
        'data/booking_check_in_email_template.xml',
        'data/booking_return_email_template.xml',
        'views/reservation_notification_config_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
