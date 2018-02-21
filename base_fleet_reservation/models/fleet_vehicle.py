# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    car_taken_minute = fields.Float(
        string='Grace Checkin.period',
        copy=True,
        help="How many minutes can a car be taken early?",
    )
    is_allowed_friend_family = fields.Boolean(
        string="Allow Friend Family",
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product For KM",
    )
    product_hour_id = fields.Many2one(
        'product.product',
        string="Product For Hour",
    )
    billing_multiplier = fields.Float(
        string="Billing Mutiplier",
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account",
    )
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag',
        string="Analytic Tags",
    )
    
    @api.model
    def create(self, vals):
        analytic_account_obj = self.env['account.analytic.account']
        result = super(FleetVehicle, self).create(vals)
        model = self.env['fleet.vehicle.model'].browse(vals.get('model_id'))
        analytic_account_vals = {
            'name': model.name +" - "+vals.get('license_plate'),
            'company_id': self.env.user.company_id.id,
            'tag_ids': [(6,0,result.analytic_tag_ids.ids)],
        }
        result.analytic_account_id = analytic_account_obj.create(analytic_account_vals)
        return result

    @api.multi
    def act_show_reservations(self):
        schedule_ids = self.env['vehicle.reservation.schedule'].search(
            [('vehicle_id', '=', self.id)])
        return {
            'name': _('Reservation Schedule'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vehicle.reservation.schedule',
            'view_id': False,
            'domain': [('id', 'in', schedule_ids.ids)],
            'target': 'current',
        }

    @api.multi
    def act_show_events(self):
        event_ids = self.env['calendar.event'].search(
            [('vehicle_id', '=', self.id)])
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        action['domain'] = [('id', 'in', event_ids.ids)]
        return action

    @api.multi
    def act_show_invoices(self):
        invoice_line_ids = self.env['account.invoice.line'].search(
            [('vehicle_id', '=', self.id)])
        invoice_ids = invoice_line_ids.filtered(lambda r: r.invoice_id)
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['domain'] = [('id', 'in', invoice_ids.ids)]
        return action

    @api.multi
    def act_show_expense(self):
        expense_ids = self.env['hr.expense'].search([('vehicle_id', '=', self.id)])
        action = self.env.ref('hr_expense.hr_expense_actions_my_unsubmitted').read()[0]
        action['context'] = ""
        action['domain'] = [('id', 'in', expense_ids.ids)]
        return action

    @api.multi
    def act_show_analityc_acc(self):
        analytic_account_ids = self.env['account.analytic.account'].search([('id', 'in', self.analytic_account_id.ids)])
        action = self.env.ref('analytic.action_account_analytic_account_form').read()[0]
        action['domain'] = [('id', 'in', analytic_account_ids.ids)]
        return action
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
