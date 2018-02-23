# -*- coding: utf-8 -*-

from odoo import fields, models, api

class HrDepartment(models.Model):
    _inherit = "hr.department"
    
    hou_user_id = fields.Many2one(
        'res.users',
        string="Head of Unit",
    )
    max_vehicle_perunit = fields.Integer(
        string="Max Vehicle Per Unit",
    )
    
    @api.multi
    def action_vehicle_reservation(self):
        for rec in self:
            reservation_ids = rec.env['fleet.vehicle.reservation'].search([('department_id', '=' ,rec.id)])
            action = rec.env.ref("base_fleet_reservation.action_fleet_vehicle_reservation").read()[0]
            action['domain'] = [('id', 'in', reservation_ids.ids)]
            return action
    
    @api.multi
    def action_account_invoice_view(self):
        for rec in self:
            invoice_ids = rec.env['account.invoice'].search([('department_id', '=' ,rec.id)])
            action = rec.env.ref("account.action_invoice_tree1").read()[0]
            action['domain'] = [('id', 'in', invoice_ids.ids)]
            return action
