# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

import pytz
import datetime
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RecieveVehicleWiz(models.TransientModel):
    _name = "recieve.vehicle.wiz"

    check_in_datetime = fields.Datetime(
        string="Check in Date",
        required=True,
    )
    recieve_employee_id = fields.Many2one(
        'hr.employee',
        string="Recieve By",
        required=True,
    )
    
    def _car_taken_early(self,event_id):
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        event_start_date = datetime.datetime.strptime(
                event_id.start,
                '%Y-%m-%d %H:%M:%S'
        )
        check_in_date = datetime.datetime.strptime(
                self.check_in_datetime,
                '%Y-%m-%d %H:%M:%S'
        )
        
        tzone_start_date = pytz.UTC.localize(event_start_date)
        start_date_tz = tzone_start_date.astimezone(timezone)
        tzone_check_in_date = pytz.UTC.localize(check_in_date)
        check_in_date_tz = tzone_check_in_date.astimezone(timezone)
        if start_date_tz.date() != check_in_date_tz.date():
            raise ValidationError("Your Reservation at %s"%(event_start_date))
        elif start_date_tz.date() == check_in_date_tz.date() and start_date_tz.time() > check_in_date_tz.time():
            early = (start_date_tz - check_in_date_tz).seconds / 3600
            if (event_id.vehicle_id.car_taken_minute > 0.0 and early > event_id.vehicle_id.car_taken_minute) or (self.env.user.company_id.car_taken_minute > 0.0 and early > self.env.user.company_id.car_taken_minute):
                raise ValidationError("You are not allowed to taken Car early before Reservation or Allowed by company to taken early limit")
        return True

    @api.multi
    def action_recieve_vehicle(self):
        event_id = self.env['calendar.event'].browse(
            int(self._context['active_id'])
        )
        car_taken_early = self._car_taken_early(event_id)
        if event_id:
            event_id.check_in_datetime = self.check_in_datetime
            event_id.recieve_employee_id = self.recieve_employee_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
