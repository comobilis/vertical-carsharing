# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    custom_employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        copy=True,
    )
    custom_department_id = fields.Many2one(
        'hr.department',
        string='Department',
        copy=True,
    )
    
    @api.onchange('custom_employee_id')
    def onchange_employee(self):
        for rec in self:
            rec.custom_department_id = rec.custom_employee_id.department_id.id