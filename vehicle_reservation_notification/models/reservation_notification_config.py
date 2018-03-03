# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class ReservationNotificationConfig(models.Model):
    _name = "reservation.notification.config"

    hour_schedule = fields.Integer(
        string="Reminder Hour",
#        required=True,
        default=1,
    )
    email_template = fields.Many2one(
        'mail.template',
        string="Reservation Reminder Mail Template",
#        required=True,
        default=lambda self:self.env.ref('vehicle_reservation_notification.email_template_reservation_reminder', raise_if_not_found=False)
    )
    check_in_email_template = fields.Many2one(
        'mail.template',
        string="Check in Email Template",
        default=lambda self:self.env.ref('vehicle_reservation_notification.booking_check_in_email_template', raise_if_not_found=False)
    )
    vehicle_return_email_template = fields.Many2one(
        'mail.template',
        string="Vehicle Return Email Template",
        default=lambda self:self.env.ref('vehicle_reservation_notification.booking_return_email_template', raise_if_not_found=False)
    )
    @api.model
    def _cron_reservation_notification(self):
        notification_config_ids = self.search([])
        if notification_config_ids:
            notification_config_id = notification_config_ids[0]
            current_date = fields.Datetime.now()
            date_time = datetime.strptime(current_date, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=notification_config_id.hour_schedule)
            start_date_time = datetime.strftime(date_time,'%Y-%m-%d %H:00:00')
            end_date_time = datetime.strptime(start_date_time, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=1)
            enddate_time = datetime.strftime(end_date_time,DEFAULT_SERVER_DATETIME_FORMAT)
            reservation_ids = self.env['vehicle.reservation.schedule'].search([('start_date_time', '>=', start_date_time),('start_date_time', '<=', enddate_time)])
            if reservation_ids:
                for reservation_id in reservation_ids:
                    email_template = notification_config_id.email_template
                    email_template.send_mail(reservation_id.id, force_send=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
