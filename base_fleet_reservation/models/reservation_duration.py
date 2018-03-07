# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

import pytz
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VehicleReservationSchedule(models.Model):
    _name = "vehicle.reservation.schedule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "fleet_vehicle_reservation_id"
#    _order = 'id desc'

    name = fields.Char(
        string="Number",
        default='New',
        copy=False,
        readonly=True,
    )
    vehicle_type_id = fields.Many2one(
        'fleet.vehicle.type',
        string="Vehicle Type",
        required=True,
    )
    vehicle_sub_type_id = fields.Many2one(
        'fleet.vehicle.sub.type',
        string="Vehicle Sub Type",
        required=True,
    )
    billing_type = fields.Selection(
        selection=[
                    ('per_km','Per KM'),
                    ('per_hr','Per Hour'),
        ],
        string="Billing Type",
        default="per_km",
    )
    department_id = fields.Many2one(
        'hr.department',
        related='fleet_vehicle_reservation_id.department_id',
        string='Department',
        store=True,
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Vehicle",
        required=True,
    )
    start_date_time = fields.Datetime(
        string="Start Date",
        required=True,
    )
    end_date_time = fields.Datetime(
        string="End Date",
        required=True,
    )
    fleet_vehicle_reservation_id = fields.Many2one(
        'fleet.vehicle.reservation',
        string='Vehicle Reservation',
    )
    reservation_date = fields.Date(
        string="Reservation Date",
        related="fleet_vehicle_reservation_id.create_date",
        store=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        related="fleet_vehicle_reservation_id.reserving_employee_id",
        string="Employee",
        store=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        related="fleet_vehicle_reservation_id.partner_id",
        store=True,
    )
    invoice_partner_id = fields.Many2one(
        'res.partner',
        string="Invoice Partner",
        related="fleet_vehicle_reservation_id.invoice_partner_id",
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        related="fleet_vehicle_reservation_id.company_id",
        store=True,
    )
    calendar_event_id = fields.Many2one(
        'calendar.event',
        string="Reservation Events",
    )
    is_return = fields.Boolean(
        string='Is Return ?',
        related="calendar_event_id.is_return",
        readonly=True,
        store=True,
    )
    total_km = fields.Float(
        string="Return Actual K/M",
        related="calendar_event_id.total_km",
        readonly=True,
        store=True,
    )
    total_hour = fields.Float(
        string="Return Actual H/R",
        related="calendar_event_id.total_hour",
        readonly=True,
        store=True,
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        string="Invoice",
        readonly=True,
    )
    invoice_amount_to_pay = fields.Float(
        string="Amount to Pay",
        compute="_compute_amount_to_pay",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )
    invoice_state = fields.Selection(
        string='Invoice Status',
        related="invoice_id.state",
    )
    prolog_hours = fields.Float(
        string="Prolog Hours",
    )
    extra_time_no_reservation = fields.Boolean(
        string="Extra Time & No Other Reservation",
    )
    is_invoice_created = fields.Boolean(
        string="Invoice Created",
        compute="_compute_invoice_created",
        store=True,
    )
    is_service_vehicle_reservation = fields.Boolean(
        string="This reservation is to be able to Service the vehicle",
        related="fleet_vehicle_reservation_id.is_service_vehicle_reservation",
        store=True,
    )
#    reservation_service_type_id = fields.Many2one(
#        'fleet.service.type',
#        string="Service Type",
#    )

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            if vals.get('name', 'New') != 'New':
                vals['name'] = 'New'

        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence']\
                .next_by_code('vehicle.reservation.schedule') or 'New'
        result = super(VehicleReservationSchedule, self).create(vals)
        result.name = result.fleet_vehicle_reservation_id.name + ' - ' + result.name
        return result

    @api.onchange('end_date_time')
    def end_date_time_change(self):
        for rec in self:
            if rec.start_date_time and rec.end_date_time and rec.vehicle_id:
                start_date = datetime.datetime.strptime(
                    rec.start_date_time,
                    '%Y-%m-%d %H:%M:%S'
                )
                timezone = pytz.timezone(self._context.get('tz') or 'UTC')
                end_date = datetime.datetime.strptime(
                    rec.end_date_time,
                    '%Y-%m-%d %H:%M:%S'
                )
                if end_date < start_date:
                    raise ValidationError(_(
                        'Ending datetime cannot be set before starting\
                         datetime.'
                    ))
                if rec.vehicle_id.reserve_period == 'some_time':
                    avail_from = '{0:02.0f}:{1:02.0f}'.\
                        format(*divmod(
                            rec.vehicle_id.available_from * 60,
                            60))
                    avail_to = '{0:02.0f}:{1:02.0f}'.\
                        format(*divmod(
                            rec.vehicle_id.available_to * 60,
                            60))

                    tzone_start_date = pytz.UTC.localize(start_date)
                    start_date_tz = tzone_start_date.astimezone(timezone)

                    tzone_end_date = pytz.UTC.localize(end_date)
                    end_date_tz = tzone_end_date.astimezone(timezone)

                    if not (str(start_date_tz.time()) >= str(avail_from) and
                            str(start_date_tz.time()) <= str(avail_to)):
                        raise ValidationError(_("This vehicle is available\
                                    for %s to %s." % (avail_from, avail_to)))

                    elif not (str(end_date_tz.time()) >= str(avail_from) and
                              str(end_date_tz.time()) <= str(avail_to)):
                        raise ValidationError(_("This vehicle is available\
                                    for %s to %s." % (avail_from, avail_to)))

                elif rec.vehicle_id.reserve_period == 'not_avail':
                    avail_from = '{0:02.0f}:{1:02.0f}'.\
                        format(*divmod(
                            rec.vehicle_id.not_available_from * 60,
                            60))
                    avail_to = '{0:02.0f}:{1:02.0f}'.\
                        format(*divmod(
                            rec.vehicle_id.not_available_to * 60,
                            60))

                    tzone_start_date = pytz.UTC.localize(start_date)
                    start_date_tz = tzone_start_date.astimezone(timezone)

                    tzone_end_date = pytz.UTC.localize(end_date)
                    end_date_tz = tzone_end_date.astimezone(timezone)

                    if str(start_date_tz.time()) >= str(avail_from) and\
                            str(start_date_tz.time()) <= str(avail_to):
                        raise ValidationError(_("This vehicle is not\
available for %s to %s." % (avail_from, avail_to)))
                    elif str(end_date_tz.time()) >= str(avail_from) and\
                            str(end_date_tz.time()) <= str(avail_to):
                        raise ValidationError(_("This vehicle is not\
available for %s to %s." % (avail_from, avail_to)))

                event_ids = self.env['calendar.event'].search(
                    [('vehicle_id', '=', rec.vehicle_id.id), ('is_return', '=', False)]
                )
                for event in event_ids:
                    if event.start_datetime >= rec.start_date_time and\
                            event.start_datetime <= rec.end_date_time:
                        raise ValidationError(_("This vehicle is already\
                        reserved on your selected date."))
                    elif event.stop_datetime >= rec.start_date_time and\
                            event.stop_datetime <= rec.end_date_time:
                        raise ValidationError(_("This vehicle is already\
reserved on your selected date."))

    @api.depends("invoice_id", "invoice_id.state")
    def _compute_invoice_created(self):
        for rec in self:
            if not rec.invoice_id or rec.invoice_id.state == 'cancel':
                rec.is_invoice_created = False
            else:
                rec.is_invoice_created = True

    @api.depends("total_km","total_hour")
    def _compute_amount_to_pay(self):
        for rec in self:
            cost_ids = rec.vehicle_id.vehicle_dest_cost_ids
            time_cost_ids = rec.vehicle_id.vehicle_time_cost_ids
            amount = 0.0
            if rec.billing_type == "per_km":
                for cost in cost_ids:
                    if rec.total_km >= cost.from_dist and\
                            rec.total_km <= cost.to_dist:
                        amount = cost.price_km * rec.total_km
                    else:
                        max_dist =  max([cost.to_dist for cost in cost_ids])
                        cost_id = cost_ids.search([('to_dist','=',max_dist)])
                        amount = rec.company_id.currency_id.compute(cost.price_km * rec.total_km, rec.fleet_vehicle_reservation_id.currency_id)
                rec.invoice_amount_to_pay = amount
            elif rec.billing_type == "per_hr":
                for cost in time_cost_ids:
                    if rec.total_km >= cost.from_hour and\
                            rec.total_km <= cost.to_hour:
                        amount = cost.price_hour * rec.total_km
                    else:
                        max_hr =  max([cost.to_hour for cost in time_cost_ids])
                        cost_id = time_cost_ids.search([('to_hour','=',max_hr)])
                        amount = rec.company_id.currency_id.compute(cost_id.price_hour * rec.total_hour, rec.fleet_vehicle_reservation_id.currency_id)
            rec.invoice_amount_to_pay = amount
