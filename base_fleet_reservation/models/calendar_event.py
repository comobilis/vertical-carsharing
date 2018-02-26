# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    vehicle_type_id = fields.Many2one(
        'fleet.vehicle.type',
        string="Vehicle Type",
        readonly=True,
    )
    vehicle_sub_type_id = fields.Many2one(
        'fleet.vehicle.sub.type',
        string="Vehicle Sub Type",
        readonly=True,
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Reserved Vehicle",
        store=True,
        readonly=True,
    )
    vehicle_reservation_id = fields.Many2one(
        'fleet.vehicle.reservation',
        string="Vehicle Reservation",
        readonly=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
#        readonly=True,
    )
    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'),
                   ('reserved', 'Reserved'),
                   ('cancel', 'Cancel')],
        related="vehicle_reservation_id.state",
        string="State",
        readonly=True,
        track_visibility='onchange',
    )
    reservation_schedule_id = fields.Many2one(
        'vehicle.reservation.schedule',
        string="Reservation Schedule",
        readonly=True,
    )
    is_return = fields.Boolean(
        string='Is Return ?',
        readonly=True,
    )
    total_km = fields.Float(
        string="Total K/M",
        readonly=True,
    )
    total_hour = fields.Float(
        string="Total H/R",
        readonly=True,
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        related="reservation_schedule_id.invoice_id",
        string='Invoice',
        readonly=True,
    )
    is_ride_share = fields.Boolean(
        string="I’m willing to Rideshare",
        readonly=True,
    )
    rides_msg = fields.Char(
        string="Ride Message",
        default="I’m going to",
        readonly=True,
    )
    is_service_vehicle_reservation = fields.Boolean(
        string="This reservation is to be able to Service the vehicle",
        readonly=True,
    )
    reservation_service_type_id = fields.Many2one(
        'fleet.service.type',
        string="Service Type",
        readonly=True,
    )
    is_reserve_for_other = fields.Boolean(
        string="This reservation is for Friends or Family",
        readonly=True,
    )
    employee_present_status = fields.Selection([
        ('present', 'Employee/Member Present'),
        ('absent', 'Employee/Member Not Present')],
        string="Employee Present Status",
        readonly=True,
    )
    person_phone = fields.Char(
        string='Person Phone',
        copy=True,
        readonly=True,
    )
    person_name = fields.Char(
        string="Person Name",
        readonly=True,
    )
    deposit_charge_amount = fields.Float(
        string="Deposit Amount",
        readonly=True,
    )
    vehicle_reserved_employee_id = fields.Many2one(
        'hr.employee',
        string='Vehicle Reserved By',
#        readonly=True,
    )
    #New 26_JAN_18
    check_in_datetime = fields.Datetime(
        string="Check in Date",
        readonly=True,
    )
    recieve_employee_id = fields.Many2one(
        'hr.employee',
        string="Recieve By",
        readonly=True,
    )
    return_date_time = fields.Datetime(
        string="Return Date",
        readonly=True,
    )
    return_emoployee_id = fields.Many2one(
        'hr.employee',
        string="Return By",
        readonly=True,
    )
    prolog_hours = fields.Float(
        string="Prolog Hours",
    )
    extra_time_no_reservation = fields.Boolean(
        string="Extra Time & No Other Reservation",
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self:self.env.user.company_id.id,
    )
    
    @api.onchange('vehicle_reserved_employee_id')
    def onchange_employee_id(self):
        if self.vehicle_reserved_employee_id and self.vehicle_reserved_employee_id.department_id:
            self.company_id = self.vehicle_reserved_employee_id.department_id.company_id.id

    @api.multi
    def act_show_invoices(self):
        invoice_line_ids = self.env['account.invoice.line'].search(
            [('reservation_schedule_id',
              '=',
              self.reservation_schedule_id.id)])
        invoice_ids = invoice_line_ids.filtered(lambda r: r.invoice_id)
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['domain'] = [('id', 'in', invoice_ids.ids)]
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
