# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class FleetVehicleCost(models.Model):
    _inherit = "fleet.vehicle.cost"
    
    hr_expense_id = fields.Many2one(
        'hr.expense',
        string="Expense",
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
