# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
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
    
    @api.multi
    def action_confirm(self):
        rec = super(SaleOrder, self).action_confirm()
        if self.analytic_account_id:
            self.analytic_account_id.write({'custom_employee_id': self.custom_employee_id.id,
                                            'custom_department_id': self.custom_department_id.id,
                                            })
        return rec