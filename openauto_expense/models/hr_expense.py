# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrExpenses(models.Model):
    _inherit = 'hr.expense'
    
    @api.onchange('employee_id')
    def onchange_employee(self):
        for rec in self:
            rec.custom_department_id = rec.employee_id.department_id.id
    
    vehicle_reservation_id = fields.Many2one(
        'fleet.vehicle.reservation',
        string="Vehicle Reservation",
    )
    vehicle_reservation_schedule_id = fields.Many2one(
        'vehicle.reservation.schedule',
        string="Vehicle Reservation Schedule",
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Vehicle",
        related="vehicle_reservation_schedule_id.vehicle_id",
        store=True,
    )
    custom_department_id = fields.Many2one(
        'hr.department',
        string='Department',
    )
    vehicle_cost_id = fields.Many2one(
        'fleet.vehicle.cost',
        string='Vehicle Cost',
    )

    @api.multi
    def submit_expenses(self):
        amount = 0.0
        for rec in self:
            amount += rec.total_amount
            if amount < rec.company_id.reimbursement_of_expenses:
                raise ValidationError("Total Expense is less then Company Reimbursement Amount Min")
        return super(HrExpenses, self).submit_expenses()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
