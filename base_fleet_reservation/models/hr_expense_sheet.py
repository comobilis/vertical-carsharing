# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api

class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"
    
    
    @api.multi
    def approve_expense_sheets(self):
        result = super(HrExpenseSheet, self).approve_expense_sheets()
        vehicle_cost_obj = self.env['fleet.vehicle.cost']
        service_type_id = self.env['fleet.service.type'].search([('name', '=', 'Vehicle Expense')])
        for rec in self:
            for line in rec.expense_line_ids:
                if line.vehicle_id:
                    vals={
                           'vehicle_id':line.vehicle_id.id,
                           'cost_subtype_id':service_type_id.id,
                           'amount':line.total_amount,
                           'description':line.description,
                           'date':line.date,
                           'analytic_account_id':line.analytic_account_id.id,
                           'hr_expense_id':line.id
                    }
                    vehicle_cost_id = vehicle_cost_obj.create(vals)
                    line.vehicle_cost_id = vehicle_cost_id

        return result


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
