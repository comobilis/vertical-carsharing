# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ReturnVehicleWiz(models.TransientModel):
    _name = "return.vehicle.wiz"

    return_confirmation = fields.Boolean(
        string="Is Return ? ",
    )
    total_km = fields.Float(
        string="Total K/m",
        required=True,
    )
    total_hour = fields.Integer(
        string="Total Hour",
        required=True,
    )
    return_date_time = fields.Datetime(
        string="Return Date",
        required=True,
    )
    return_emoployee_id = fields.Many2one(
        'hr.employee',
        string="Return By",
        required=True,
    )
    prolog_hours = fields.Float(
        string="Prolog Hours",
    )
    extra_time_no_reservation = fields.Boolean(
        string="Extra Time & No Other Reservation",
    )

    @api.multi
    def action_return_vehicle(self):
        if not self.return_confirmation:
            raise ValidationError("You are not sure so\
                    you can not return vehicle.")
        else:
            event_id = self.env['calendar.event'].browse(
                int(self._context['active_id'])
            )
            if event_id:
                event_id.is_return = True
                event_id.total_km = self.total_km
                event_id.return_date_time = self.return_date_time
                event_id.return_emoployee_id = self.return_emoployee_id.id
                event_id.total_hour = self.total_hour
                if self.prolog_hours and event_id.reservation_schedule_id:
                    event_id.prolog_hours = self.prolog_hours
                    event_id.extra_time_no_reservation = self.extra_time_no_reservation
                    event_id.reservation_schedule_id.prolog_hours = self.prolog_hours
                    if self.extra_time_no_reservation:
                        active_model = self._context['active_model']
                        event_ids = self.env[active_model].search([('start','<=',event_id.stop),('start','>=',fields.Datetime.now()),('is_return','=',False)])
                        if not event_ids:
                            event_id.reservation_schedule_id.extra_time_no_reservation = self.extra_time_no_reservation

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
