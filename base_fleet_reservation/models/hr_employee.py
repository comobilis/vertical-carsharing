# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    vehicle_reservation_ids = fields.One2many(
        'fleet.vehicle.reservation',
        'reserving_employee_id',
        string="Vehicle Reservation",
        readonly=True,
    )
#    open_invoice_due_date = fields.Datetime(
#        compute="_compute_due_date",
#        string="Due Date",
#    )
#    advance_payment_level_id = fields.Many2one(
#        'advance.payment.level',
#        string="Payment Level"
#    )

#    @api.model
#    def create(self, vals):
#        result = super(HrEmployee, self).create(vals)
#        if result.user_id and result.user_id.partner_id:
#            result.user_id.department_id = result.department_id.id
#            result.user_id.partner_id.department_id = result.department_id.id
#        return result
    
#    @api.multi
#    def write(self, vals):
#        result = super(HrEmployee, self).write(vals)
#        for rec in self:
#            if vals.get('department_id'):
#                rec.user_id.department_id = rec.department_id.id
#                rec.user_id.partner_id.department_id = rec.department_id.id
#        return result

#    def _compute_due_date(self):
#        for rec in self:
#            invoice_obj = rec.env['account.invoice']
#            invoice_ids = invoice_obj.search([
#                ('reservation_employee_id', '=', rec.id),
#                ('state', '=', 'open')]
#            )
#            if not invoice_ids:
#                rec.open_invoice_due_date = False
#            for invoice in invoice_ids:
#                if not rec.open_invoice_due_date:
#                    rec.open_invoice_due_date = invoice.date_due
#                elif rec.open_invoice_due_date and\
#                        rec.open_invoice_due_date > invoice.date_due:
#                        rec.open_invoice_due_date = invoice.date_due

    @api.multi
    def action_vehicle_reservation(self):
        for rec in self:
            action = rec.env.ref("base_fleet_reservation.\
            action_fleet_vehicle_reservation").read()[0]
            action['domain'] = [('id', 'in', rec.vehicle_reservation_ids.ids)]
            return action

    @api.multi
    def action_reservation_calendar(self):
        for rec in self:
            calendar_event_ids = rec.env['calendar.event'].search([
                ('vehicle_reserved_employee_id', '=', rec.id)])
            action = rec.env.ref("calendar.action_calendar_event").read()[0]
            action['domain'] = [('id', 'in', calendar_event_ids.ids)]
            return action

    @api.multi
    def action_invoice(self):
        for rec in self:
            action = rec.env.ref("account.action_invoice_tree1").read()[0]
            invoice_ids = rec.env['account.invoice'].search([
                ('reservation_employee_id', '=', rec.id)])
            action['domain'] = [('id', 'in', invoice_ids.ids)]
            return action
