# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

#    open_invoice_due_date = fields.Datetime(
#        compute="_compute_due_date",
#        string="Due Date",
#    )
#    advance_payment_level_id = fields.Many2one(
#        'advance.payment.level',
#        string="Payment Level"
#    )
#    NEW
    rfid_key = fields.Char(
        string="RFID Key",
        copy=False,
    )
    rfid_key_comp = fields.Char(
        string="RFID Key",
        copy=False,
        compute="_compute_rfid_key",
    )
    
    @api.depends("rfid_key")
    def _compute_rfid_key(self):
        for rec in self:
            rec.rfid_key_comp = rec.rfid_key
    
    @api.onchange("rfid_key")
    def _onchange_rfid_key(self):
        for rec in self:
            rec.user_id.write({'rfid_key' : rec.rfid_key})
            rec.user_id.partner_id.write({'rfid_key' : rec.rfid_key})
    

    @api.model
    def create(self, vals):
        result = super(HrEmployee, self).create(vals)
        if result.user_id and result.user_id.partner_id:
            result.user_id.department_id = result.department_id.id
            result.user_id.partner_id.department_id = result.department_id.id
        return result
        
    @api.multi
    def write(self, vals):
        result = super(HrEmployee, self).write(vals)
        for rec in self:
            if vals.get('department_id') and rec.user_id:
                rec.user_id.department_id = rec.department_id.id
                rec.user_id.partner_id.department_id = rec.department_id.id
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
