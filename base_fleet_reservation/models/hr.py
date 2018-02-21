# -*- coding: utf-8 -*-

from odoo import fields, models

class Department(models.Model):
    _inherit = "hr.department"
    
    hou_user_id = fields.Many2one(
        'res.users',
        string="Head of Unit",
    )