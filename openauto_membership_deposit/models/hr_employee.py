# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

#    rfid_key = fields.Char(
#        string="RFID Key",
#        copy=False,
#    )
#    rfid_key_comp = fields.Char(
#        string="RFID Key",
#        copy=False,
#        compute="_compute_rfid_key",
#    )
    payment_level_id = fields.Many2one(
        'membership.payment.level',
#        required=True,
        string="Membership Level",
    )

#    @api.depends("rfid_key")
#    def _compute_rfid_key(self):
#        for rec in self:
#            rec.rfid_key_comp = rec.rfid_key
#    
#    @api.onchange("rfid_key")
#    def _onchange_rfid_key(self):
#        for rec in self:
#            rec.user_id.write({'rfid_key' : rec.rfid_key})
#            rec.user_id.partner_id.write({'rfid_key' : rec.rfid_key})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
