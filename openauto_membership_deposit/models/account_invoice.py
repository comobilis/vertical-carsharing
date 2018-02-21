# -*- coding: utf-8 -*-

# Part of Openauto
#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    membership_deposit_id = fields.Many2one(
        'membership.deposit',
        string='Membership Deposit',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
