# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api

class HrExpenses(models.Model):
    _inherit = 'hr.expense'
    
    vehicle_cost_id = fields.Many2one(
        'fleet.vehicle.cost',
        string='Vehicle Cost',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
