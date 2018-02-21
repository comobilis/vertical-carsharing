# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class FleetVehicleCost(models.Model):
    _inherit = "fleet.vehicle.cost"
    
    analytic_line_id = fields.Many2one(
        'account.analytic.line',
        string="Analytic Line",
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account",
        related="vehicle_id.analytic_account_id",
    )
#    hr_expense_id = fields.Many2one(
#        'hr.expense',
#        string="Expense",
#    )
    @api.model
    def create (self, vals):
        analytic_line_obj = self.env['account.analytic.line']
        result = super(FleetVehicleCost, self).create(vals)
        if result.description:
            name=result.description
        else:
            name=result.vehicle_id.name
        analytic_line_vals = {
            'name': name ,
            'account_id': result.analytic_account_id.id,
            'amount': result.amount * -1,
            'date': result.date,
        }
        result.analytic_line_id = analytic_line_obj.create(analytic_line_vals)
        return result
        
    @api.multi
    def write(self, vals):
        for rec in self:
            if vals.get('date'):
                rec.analytic_line_id.date = vals.get('date')
            if vals.get('amount'):
                rec.analytic_line_id.amount = vals.get('amount')
            if vals.get('description'):
                rec.analytic_line_id.name = vals.get('description')
            if vals.get('analytic_account_id'):
                rec.analytic_line_id.account_id = vals.get('analytic_account_id')
        return super(FleetVehicleCost, self).write(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
