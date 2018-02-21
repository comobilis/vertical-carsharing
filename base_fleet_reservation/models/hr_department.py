# -*- coding: utf-8 -*-

from odoo import fields, models

class HrDepartment(models.Model):
    _inherit = "hr.department"
    
    hou_user_id = fields.Many2one(
        'res.users',
        string="Head of Unit",
    )
    max_vehicle_perunit = fields.Integer(
        string="Max Vehicle Per Unit",
    )
